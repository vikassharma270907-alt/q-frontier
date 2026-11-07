"""
Data contracts and provenance records for QPU hardware execution.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from pydantic import BaseModel, Field, SecretStr


@dataclass
class CalibrationSnapshot:
    backend_name: str
    provider: str
    qubit_count: int
    topology_type: str  # "All-to-All (Ion Trap)", "Heavy-Hex (Superconducting)", "Ring Lattice"
    avg_t1_us: float
    avg_t2_us: float
    single_qubit_error: float
    two_qubit_error: float
    readout_error: float
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QPUExecutionRecord:
    job_id: str
    backend_name: str
    provider: str  # "IonQ", "IBM Quantum", "Quantum Rings", "Sandia Volumetric Model"
    execution_mode: str  # "REAL_QPU", "SIMULATED_NOISE_QPU"
    timestamp: str
    shots: int
    n_qubits: int
    transpiled_circuit_depth: int
    transpiled_two_qubit_gates: int
    routing_swaps: int
    calibration_snapshot: Dict[str, Any]
    raw_shot_counts: Dict[str, int]
    quasi_distribution: Dict[str, float]
    measured_feasibility: float
    measured_approximation_ratio: float
    measured_optimal_probability: float
    selected_bitstring: str
    selected_indices: List[int]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QPUExecuteRequest(BaseModel):
    backend_target: str = Field(
        "ionq",
        description="'ionq', 'ibm', 'quantum_rings', or 'sandia'."
    )
    n_qubits: int = Field(4, ge=2, le=12, description="Register qubit width.")
    k_cardinality: int = Field(2, ge=1, le=11, description="Excitation cardinality constraint.")
    circuit_depth: int = Field(1, ge=1, le=2, description="QAOA Trotter depth p.")
    shots: int = Field(1024, ge=100, le=10000, description="Measurement shot count.")
    api_token: Optional[Union[SecretStr, str]] = Field(None, description="Optional live cloud QPU provider API token.")
