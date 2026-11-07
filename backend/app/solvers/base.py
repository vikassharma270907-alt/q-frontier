"""
Base class and data contracts for portfolio selection solvers.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class SolverResult:
    solver_name: str
    solver_type: str  # "CLASSICAL_EXACT", "CLASSICAL_HEURISTIC", "SIMULATED_QUANTUM", "REAL_QPU"
    selected_indices: List[int]
    selection_vector: List[int]
    selected_tickers: List[str]
    objective_value: float
    is_feasible: bool
    feasibility_rate: float
    approximation_ratio: float
    optimal_probability: float
    runtime_ms: float
    qubits_used: Optional[int] = None
    circuit_depth: Optional[int] = None
    two_qubit_gates: Optional[int] = None
    classical_evaluations: int = 0
    state_distribution: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
