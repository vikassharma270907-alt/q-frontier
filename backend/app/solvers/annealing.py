"""
Simulated Annealing heuristic solver with strict Hamming weight preservation.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
import numpy as np

from app.solvers.base import SolverResult
from app.finance.objective import evaluate_selection_objective


class SimulatedAnnealingSolver:
    """
    Simulated Annealing algorithm operating strictly within the feasible
    Hamming-weight K subspace using pairwise index swaps.
    """

    def __init__(
        self,
        name: str = "Simulated Annealing Heuristic",
        max_iterations: int = 350,
        initial_temp: float = 1.0,
        cooling_rate: float = 0.99
    ):
        self.name = name
        self.max_iterations = max_iterations
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    def solve(
        self,
        cov: np.ndarray,
        mu: np.ndarray,
        k_cardinality: int,
        tickers: Optional[List[str]] = None,
        lambda_risk: float = 0.5,
        x_prev: Optional[np.ndarray] = None,
        turnover_penalty: float = 0.0,
        seed: int = 42,
        ground_truth_min: Optional[float] = None,
        ground_truth_max: Optional[float] = None,
    ) -> SolverResult:
        n = len(mu)
        if tickers is None:
            tickers = [f"A{i}" for i in range(n)]

        t0 = time.perf_counter()
        rng = np.random.default_rng(seed)

        # Initial feasible state
        current_indices = set(rng.choice(n, size=k_cardinality, replace=False))
        current_x = np.zeros(n, dtype=float)
        current_x[list(current_indices)] = 1.0
        current_obj = evaluate_selection_objective(
            current_x, cov, mu, lambda_risk, x_prev, turnover_penalty
        )

        best_indices = set(current_indices)
        best_obj = current_obj
        temp = self.initial_temp
        eval_count = 1

        for it in range(self.max_iterations):
            # Propose swap: remove one active index, add one inactive index
            active_list = list(current_indices)
            inactive_list = [idx for idx in range(n) if idx not in current_indices]

            remove_idx = rng.choice(active_list)
            add_idx = rng.choice(inactive_list)

            candidate_indices = (current_indices - {remove_idx}) | {add_idx}
            candidate_x = np.zeros(n, dtype=float)
            candidate_x[list(candidate_indices)] = 1.0

            cand_obj = evaluate_selection_objective(
                candidate_x, cov, mu, lambda_risk, x_prev, turnover_penalty
            )
            eval_count += 1
            delta_e = cand_obj - current_obj

            if delta_e < 0.0 or rng.random() < np.exp(-delta_e / max(temp, 1e-8)):
                current_indices = candidate_indices
                current_obj = cand_obj
                if current_obj < best_obj:
                    best_obj = current_obj
                    best_indices = set(current_indices)

            temp *= self.cooling_rate

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        best_x = np.zeros(n, dtype=int)
        best_x[list(best_indices)] = 1
        selected_indices = sorted(list(best_indices))
        selected_tickers = [tickers[i] for i in selected_indices]

        # Calculate approximation ratio if ground truth supplied
        ar = 1.0
        if ground_truth_min is not None and ground_truth_max is not None:
            e_range = max(ground_truth_max - ground_truth_min, 1e-8)
            ar = float(np.clip((ground_truth_max - best_obj) / e_range, 0.0, 1.0))

        return SolverResult(
            solver_name=self.name,
            solver_type="CLASSICAL_HEURISTIC",
            selected_indices=selected_indices,
            selection_vector=best_x.tolist(),
            selected_tickers=selected_tickers,
            objective_value=float(best_obj),
            is_feasible=True,
            feasibility_rate=1.0,
            approximation_ratio=round(ar, 4),
            optimal_probability=1.0 if (ground_truth_min is not None and np.isclose(best_obj, ground_truth_min, atol=1e-5)) else 0.0,
            runtime_ms=round(elapsed_ms, 3),
            qubits_used=None,
            circuit_depth=None,
            two_qubit_gates=None,
            classical_evaluations=eval_count,
            metadata={"seed": seed, "iterations": self.max_iterations}
        )
