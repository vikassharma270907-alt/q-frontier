"""
Hardware-calibrated QPU Solver sampling measurement shots under realistic device noise models.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Optional
import numpy as np

from app.solvers.base import SolverResult
from app.hardware.driver import qpu_driver
from app.finance.objective import evaluate_selection_objective


class QPUSolver:
    """
    QPU Hardware Solver.
    Transpiles QAOA circuit to target device topology and samples shots
    under calibrated device noise models (IonQ, IBM, Quantum Rings, Sandia).
    """

    def __init__(
        self,
        name: str = "QPU Hardware (Calibrated Device)",
        backend_target: str = "ionq",
        shots: int = 1024
    ):
        self.name = name
        self.backend_target = backend_target
        self.shots = shots

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
        opt_bitstring: Optional[str] = None,
    ) -> SolverResult:
        n = len(mu)
        if tickers is None:
            tickers = [f"A{i}" for i in range(n)]

        t0 = time.perf_counter()

        # Execute on hardware driver
        record = qpu_driver.execute_on_qpu(
            cov=cov,
            mu=mu,
            k_cardinality=k_cardinality,
            backend_target=self.backend_target,
            circuit_depth=depth,
            shots=self.shots,
            lambda_risk=lambda_risk,
            ground_truth_min=ground_truth_min,
            ground_truth_max=ground_truth_max,
            opt_bitstring=opt_bitstring,
        )

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        best_x = [int(c) for c in record.selected_bitstring]
        selected_indices = [i for i, v in enumerate(best_x) if v == 1]
        selected_tickers = [tickers[i] for i in selected_indices]

        sampled_obj = evaluate_selection_objective(
            np.array(best_x, dtype=float),
            cov,
            mu,
            lambda_risk,
            x_prev,
            turnover_penalty
        )

        # Build state distribution from quasi distribution
        state_dist = []
        for b_str, prob in sorted(record.quasi_distribution.items(), key=lambda item: item[1], reverse=True)[:10]:
            state_dist.append({
                "bitstring": b_str,
                "probability": prob,
                "is_optimal": bool(opt_bitstring and b_str == opt_bitstring)
            })

        return SolverResult(
            solver_name=f"QPU: {record.backend_name}",
            solver_type=record.execution_mode,
            selected_indices=selected_indices,
            selection_vector=best_x,
            selected_tickers=selected_tickers,
            objective_value=round(float(sampled_obj), 5),
            is_feasible=bool(len(selected_indices) == k_cardinality),
            feasibility_rate=record.measured_feasibility,
            approximation_ratio=record.measured_approximation_ratio,
            optimal_probability=record.measured_optimal_probability,
            runtime_ms=round(elapsed_ms, 3),
            qubits_used=n,
            circuit_depth=record.transpiled_circuit_depth,
            two_qubit_gates=record.transpiled_two_qubit_gates,
            classical_evaluations=1,
            state_distribution=state_dist,
            metadata={
                "job_id": record.job_id,
                "provider": record.provider,
                "backend_name": record.backend_name,
                "shots": self.shots,
                "routing_swaps": record.routing_swaps,
                "calibration_snapshot": record.calibration_snapshot,
                "raw_shot_counts_sample": dict(list(record.raw_shot_counts.items())[:8])
            }
        )
