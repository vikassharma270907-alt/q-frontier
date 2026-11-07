"""
Constraint-preserving XY-QAOA solver initialized in Dicke states.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

from app.solvers.base import SolverResult
from app.finance.objective import (
    evaluate_selection_objective,
    compute_all_bitstring_energies,
)

# 1-qubit Pauli matrices
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def create_n_qubit_operator(single_qubit_ops: Dict[int, np.ndarray], n_qubits: int) -> np.ndarray:
    """Builds tensor product matrix across n qubits."""
    op_list = [single_qubit_ops.get(i, I2) for i in range(n_qubits)]
    res = op_list[0]
    for op in op_list[1:]:
        res = np.kron(res, op)
    return res


def prepare_dicke_statevector(n_qubits: int, k_weight: int) -> np.ndarray:
    """Constructs exact Dicke state |D_K^N> as uniform superposition over Hamming weight K."""
    dim = 2 ** n_qubits
    state = np.zeros(dim, dtype=complex)
    valid_indices = [
        i for i in range(dim)
        if bin(i)[2:].zfill(n_qubits).count("1") == k_weight
    ]
    amp = 1.0 / np.sqrt(len(valid_indices))
    for idx in valid_indices:
        state[idx] = amp
    return state


def build_xy_mixer_matrix(n_qubits: int) -> np.ndarray:
    """
    Builds complete-graph XY Mixer Hamiltonian:
    H_M^{XY} = sum_{i < j} (X_i X_j + Y_i Y_j).
    Commutes strictly with total Hamming weight sum_i Z_i.
    """
    dim = 2 ** n_qubits
    h_xy = np.zeros((dim, dim), dtype=complex)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            xx = create_n_qubit_operator({i: X, j: X}, n_qubits)
            yy = create_n_qubit_operator({i: Y, j: Y}, n_qubits)
            h_xy += xx + yy
    return h_xy


class XYQAOASolver:
    """
    Hamming-weight preserving XY-QAOA simulator solver.
    """

    def __init__(self, name: str = "XY-QAOA (Simulated)"):
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

        # Ground truth within feasible Hamming weight k
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

        # Optimize variational angles
        dt = 0.8
        gamma_init = [(l / depth) * dt for l in range(1, depth + 1)]
        beta_init = [(1.0 - (l / depth)) * dt for l in range(1, depth + 1)]

        # Precompute spectral decomposition of mixer to eliminate O(2^3N) matrix exponentials
        w_m, v_m = np.linalg.eigh(h_m_xy)
        v_m_dag = v_m.conj().T

        eval_count = 0

        def loss_fn(params):
            nonlocal eval_count
            eval_count += 1
            g = params[:depth]
            b = params[depth:]
            psi = dicke_state.copy()
            for l in range(depth):
                # Diagonal Hamiltonian phase rotation O(dim)
                psi = np.exp(-1j * g[l] * energy_vec) * psi
                # Precomputed spectral evolution O(dim^2)
                psi = v_m @ (np.exp(-1j * b[l] * w_m) * (v_m_dag @ psi))
            probs = np.abs(psi) ** 2
            return float(np.dot(probs, energy_vec))

        res = minimize(
            loss_fn,
            np.array(gamma_init + beta_init),
            method="COBYLA",
            options={"maxiter": 40}
        )

        opt_params = res.x
        psi_final = dicke_state.copy()
        for l in range(depth):
            psi_final = np.exp(-1j * opt_params[l] * energy_vec) * psi_final
            psi_final = v_m @ (np.exp(-1j * opt_params[depth + l] * w_m) * (v_m_dag @ psi_final))

        probs = np.abs(psi_final) ** 2
        exp_energy = float(np.dot(probs, energy_vec))
        feasibility = float(np.sum(probs[feasible_mask]))
        p_opt = float(probs[opt_idx])
        ar = float(np.clip((e_max - exp_energy) / e_range, 0.0, 1.0))

        # Most probable feasible state
        best_prob_feasible_idx = feasible_indices[np.argmax(probs[feasible_mask])]
        best_bitstring = bitstrings[best_prob_feasible_idx]
        best_x = [int(c) for c in best_bitstring]
        selected_indices = [i for i, v in enumerate(best_x) if v == 1]
        selected_tickers = [tickers[i] for i in selected_indices]
        sampled_best_obj = float(energy_vec[best_prob_feasible_idx])

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

        two_qubit_gates = int(n * (n - 1) * depth)

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
            circuit_depth=depth * 4,
            two_qubit_gates=two_qubit_gates,
            classical_evaluations=eval_count,
            state_distribution=state_dist,
            metadata={
                "depth": depth,
                "expected_energy": exp_energy,
                "gamma": [float(x) for x in opt_params[:depth]],
                "beta": [float(x) for x in opt_params[depth:]],
                "backend": "statevector_exact_simulated",
            }
        )
