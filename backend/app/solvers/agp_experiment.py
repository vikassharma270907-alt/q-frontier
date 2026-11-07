"""
Counterdiabatic CCD-QAOA with 3-body Adiabatic Gauge Potential (AGP) shortcuts.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

from app.solvers.base import SolverResult
from app.solvers.xy_qaoa import (
    prepare_dicke_statevector,
    build_xy_mixer_matrix,
)
from app.finance.objective import (
    evaluate_selection_objective,
    compute_all_bitstring_energies,
)


def build_agp_counterdiabatic_matrix(h_c: np.ndarray, h_m: np.ndarray) -> np.ndarray:
    """
    Calculates the 3-body Adiabatic Gauge Potential (AGP) generator:
    H_CD = i * [H_C, H_M] / || [H_C, H_M] ||_2.
    """
    commutator = 1j * (h_c @ h_m - h_m @ h_c)
    norm = np.linalg.norm(commutator, ord=2)
    if norm < 1e-12:
        return np.zeros_like(commutator)
    return commutator / norm


class CounterdiabaticQAOASolver:
    """
    Constrained Counterdiabatic QAOA (CCD-QAOA) Solver.
    Uses Dicke state, XY-mixer, and normalized 3-body commutator AGP drive.
    """

    def __init__(self, name: str = "CCD-QAOA (Counterdiabatic AGP, Simulated)"):
        self.name = name

    def solve(
        self,
        cov: np.ndarray,
        mu: np.ndarray,
        k_cardinality: int,
        tickers: Optional[List[str]] = None,
        lambda_risk: float = 0.5,
        depth: int = 1,
        x_prev: Optional[np.ndarray] = None,
        turnover_penalty: float = 0.0,
        ground_truth_min: Optional[float] = None,
        ground_truth_max: Optional[float] = None,
    ) -> SolverResult:
        n = len(mu)
        if tickers is None:
            tickers = [f"A{i}" for i in range(n)]

        t0 = time.perf_counter()
        dim = 2 ** n

        dicke_state = prepare_dicke_statevector(n, k_cardinality)
        h_m_xy = build_xy_mixer_matrix(n)

        energy_vec, bitstrings = compute_all_bitstring_energies(
            cov, mu, lambda_risk, x_prev, turnover_penalty
        )
        h_c = np.diag(energy_vec).astype(complex)
        h_cd = build_agp_counterdiabatic_matrix(h_c, h_m_xy)

        feasible_mask = np.zeros(dim, dtype=bool)
        for i in range(dim):
            if bitstrings[i].count("1") == k_cardinality:
                feasible_mask[i] = True

        feasible_indices = np.where(feasible_mask)[0]
        feasible_energies = energy_vec[feasible_mask]
        e_min = float(np.min(feasible_energies))
        e_max = float(np.max(feasible_energies))
        e_range = max(e_max - e_min, 1e-8)
        opt_idx = feasible_indices[np.argmin(feasible_energies)]

        dt = 0.8
        gamma_init = [(l / depth) * dt for l in range(1, depth + 1)]
        beta_init = [(1.0 - (l / depth)) * dt for l in range(1, depth + 1)]
        alpha_init = [0.25 / depth] * depth

        eval_count = 0

        def loss_fn(params):
            nonlocal eval_count
            eval_count += 1
            g = params[:depth]
            b = params[depth:2*depth]
            a = params[2*depth:]

            psi = dicke_state.copy()
            for l in range(depth):
                u_c = expm(-1j * g[l] * h_c)
                u_m = expm(-1j * b[l] * h_m_xy)
                u_cd = expm(-1j * a[l] * h_cd)
                psi = u_cd @ (u_m @ (u_c @ psi))

            probs = np.abs(psi) ** 2
            return float(np.dot(probs, energy_vec))

        init_params = np.array(gamma_init + beta_init + alpha_init)
        res = minimize(loss_fn, init_params, method="COBYLA", options={"maxiter": 60})

        opt_params = res.x
        psi_final = dicke_state.copy()
        for l in range(depth):
            u_c = expm(-1j * opt_params[l] * h_c)
            u_m = expm(-1j * opt_params[depth + l] * h_m_xy)
            u_cd = expm(-1j * opt_params[2 * depth + l] * h_cd)
            psi_final = u_cd @ (u_m @ (u_c @ psi_final))

        probs = np.abs(psi_final) ** 2
        exp_energy = float(np.dot(probs, energy_vec))
        feasibility = float(np.sum(probs[feasible_mask]))
        p_opt = float(probs[opt_idx])
        ar = float(np.clip((e_max - exp_energy) / e_range, 0.0, 1.0))

        best_prob_idx = feasible_indices[np.argmax(probs[feasible_mask])]
        best_bitstring = bitstrings[best_prob_idx]
        best_x = [int(c) for c in best_bitstring]
        selected_indices = [i for i, v in enumerate(best_x) if v == 1]
        selected_tickers = [tickers[i] for i in selected_indices]
        sampled_best_obj = float(energy_vec[best_prob_idx])

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        state_dist = []
        for i in feasible_indices:
            state_dist.append({
                "bitstring": bitstrings[i],
                "energy": round(float(energy_vec[i]), 5),
                "probability": round(float(probs[i]), 5),
                "is_optimal": bool(i == opt_idx)
            })

        two_qubit_gates = int(n * (n - 1) * depth * 2)

        return SolverResult(
            solver_name=self.name,
            solver_type="SIMULATED_QUANTUM",
            selected_indices=selected_indices,
            selection_vector=best_x,
            selected_tickers=selected_tickers,
            objective_value=sampled_best_obj,
            is_feasible=True,
            feasibility_rate=round(feasibility, 4),
            approximation_ratio=round(ar, 4),
            optimal_probability=round(p_opt, 4),
            runtime_ms=round(elapsed_ms, 3),
            qubits_used=n,
            circuit_depth=depth * 6,
            two_qubit_gates=two_qubit_gates,
            classical_evaluations=eval_count,
            state_distribution=state_dist,
            metadata={
                "depth": depth,
                "agp_commutator_active": True,
                "expected_energy": exp_energy,
                "backend": "statevector_exact_simulated",
            }
        )
