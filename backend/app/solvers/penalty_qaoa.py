"""
Standard Penalty-QAOA solver demonstrating shot leakage under unconstrained mixers.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
import numpy as np
from scipy.linalg import expm

from app.solvers.base import SolverResult
from app.solvers.xy_qaoa import X, create_n_qubit_operator
from app.finance.objective import (
    evaluate_selection_objective,
    compute_all_bitstring_energies,
)


class PenaltyQAOASolver:
    """
    Standard QAOA using transverse field mixer H_M^X = sum_i X_i and
    quadratic penalty term rho * (sum(x_i) - K)^2.
    Demonstrates constraint violation and shot leakage.
    """

    def __init__(self, name: str = "Penalty-QAOA (Transverse Mixer)", penalty_weight: float = 2.0):
        self.name = name
        self.penalty_weight = penalty_weight

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

        energy_vec, bitstrings = compute_all_bitstring_energies(
            cov, mu, lambda_risk, x_prev, turnover_penalty
        )

        feasible_mask = np.zeros(dim, dtype=bool)
        h_pen_vec = np.zeros(dim, dtype=float)

        for i in range(dim):
            w = bitstrings[i].count("1")
            if w == k_cardinality:
                feasible_mask[i] = True
            h_pen_vec[i] = energy_vec[i] + self.penalty_weight * ((w - k_cardinality) ** 2)

        feasible_indices = np.where(feasible_mask)[0]
        feasible_energies = energy_vec[feasible_mask]
        e_min = float(np.min(feasible_energies))
        e_max = float(np.max(feasible_energies))
        e_range = max(e_max - e_min, 1e-8)
        opt_idx = feasible_indices[np.argmin(feasible_energies)]

        # Exact transverse field mixer unitary: exp(-i*beta*sum X_i) = kron_{i=1}^n (cos(beta)*I - i*sin(beta)*X)
        beta = 0.5
        gamma = 0.5
        u1 = np.array([
            [np.cos(beta), -1j * np.sin(beta)],
            [-1j * np.sin(beta), np.cos(beta)]
        ], dtype=complex)

        u_m = u1
        for _ in range(n - 1):
            u_m = np.kron(u_m, u1)

        # Initial state |+>^N
        psi = np.ones(dim, dtype=complex) / np.sqrt(dim)

        # Evolution at fixed shallow angle
        for _ in range(depth):
            # Diagonal phase rotation O(dim)
            psi = np.exp(-1j * gamma * h_pen_vec) * psi
            # Transverse mixer evolution O(dim^2)
            psi = u_m @ psi

        probs = np.abs(psi) ** 2
        feasibility_rate = float(np.sum(probs[feasible_mask]))

        # Conditional expectation on feasible subspace
        if feasibility_rate > 1e-6:
            cond_energy = float(np.dot(probs[feasible_mask], feasible_energies) / feasibility_rate)
            ar = float(np.clip((e_max - cond_energy) / e_range, 0.0, 1.0))
        else:
            cond_energy = e_max
            ar = 0.0

        p_opt = float(probs[opt_idx])

        # Most probable feasible state
        best_prob_idx = feasible_indices[np.argmax(probs[feasible_mask])]
        best_bitstring = bitstrings[best_prob_idx]
        best_x = [int(c) for c in best_bitstring]
        selected_indices = [i for i, v in enumerate(best_x) if v == 1]
        selected_tickers = [tickers[i] for i in selected_indices]
        sampled_obj = float(energy_vec[best_prob_idx])

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        # Distribution snippet
        state_dist = []
        for i in feasible_indices:
            state_dist.append({
                "bitstring": bitstrings[i],
                "energy": round(float(energy_vec[i]), 5),
                "probability": round(float(probs[i]), 5),
                "is_optimal": bool(i == opt_idx)
            })

        return SolverResult(
            solver_name=self.name,
            solver_type="SIMULATED_QUANTUM",
            selected_indices=selected_indices,
            selection_vector=best_x,
            selected_tickers=selected_tickers,
            objective_value=sampled_obj,
            is_feasible=True,
            feasibility_rate=round(feasibility_rate, 4),
            approximation_ratio=round(ar, 4),
            optimal_probability=round(p_opt, 4),
            runtime_ms=round(elapsed_ms, 3),
            qubits_used=n,
            circuit_depth=depth * 2,
            two_qubit_gates=0,  # Single-qubit X mixer
            classical_evaluations=1,
            state_distribution=state_dist,
            metadata={
                "penalty_weight": self.penalty_weight,
                "shot_leakage_pct": round((1.0 - feasibility_rate) * 100.0, 2),
                "backend": "statevector_exact_simulated",
            }
        )
