"""
Exact combinatorial enumeration solver providing mathematical ground truth for small N <= 16.
"""

from __future__ import annotations
import itertools
import time
from typing import List, Dict, Any, Optional
import numpy as np

from app.solvers.base import SolverResult
from app.finance.objective import evaluate_selection_objective


class ExactEnumerationSolver:
    """
    Evaluates all binom(N, K) feasible asset combinations to establish
    exact minimum objective, optimal selection, and worst feasible objective.
    """

    def __init__(self, name: str = "Exact Classical Enumeration"):
        self.name = name

    def solve(
        self,
        cov: np.ndarray,
        mu: np.ndarray,
        k_cardinality: int,
        tickers: Optional[List[str]] = None,
        lambda_risk: float = 0.5,
        x_prev: Optional[np.ndarray] = None,
        turnover_penalty: float = 0.0
    ) -> SolverResult:
        n = len(mu)
        if tickers is None:
            tickers = [f"A{i}" for i in range(n)]

        t0 = time.perf_counter()
        best_obj = float("inf")
        worst_obj = float("-inf")
        best_combination = None
        eval_count = 0

        for comb in itertools.combinations(range(n), k_cardinality):
            eval_count += 1
            x = np.zeros(n, dtype=float)
            x[list(comb)] = 1.0
            obj = evaluate_selection_objective(
                x, cov, mu, lambda_risk, x_prev, turnover_penalty
            )
            if obj < best_obj:
                best_obj = obj
                best_combination = comb
            if obj > worst_obj:
                worst_obj = obj

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        best_x = np.zeros(n, dtype=int)
        if best_combination is not None:
            best_x[list(best_combination)] = 1

        selected_indices = list(best_combination) if best_combination is not None else []
        selected_tickers = [tickers[i] for i in selected_indices]

        return SolverResult(
            solver_name=self.name,
            solver_type="CLASSICAL_EXACT",
            selected_indices=selected_indices,
            selection_vector=best_x.tolist(),
            selected_tickers=selected_tickers,
            objective_value=float(best_obj),
            is_feasible=True,
            feasibility_rate=1.0,
            approximation_ratio=1.0,
            optimal_probability=1.0,
            runtime_ms=round(elapsed_ms, 3),
            qubits_used=None,
            circuit_depth=None,
            two_qubit_gates=None,
            classical_evaluations=eval_count,
            metadata={
                "total_combinations_checked": eval_count,
                "e_min": float(best_obj),
                "e_max": float(worst_obj),
                "e_range": float(max(worst_obj - best_obj, 1e-8)),
            }
        )
