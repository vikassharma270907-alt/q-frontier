"""
Computational and quantum circuit resource estimation across hardware topologies.
"""

from __future__ import annotations
from typing import Dict, Any


def estimate_circuit_resources(
    n_qubits: int,
    depth: int = 1,
    include_agp: bool = False
) -> Dict[str, Any]:
    """
    Estimates theoretical circuit resources for complete-graph XY mixer QAOA
    comparing all-to-all connectivity (IonQ) vs sparse heavy-hex (IBM).
    """
    k_pairs = int(n_qubits * (n_qubits - 1) / 2)
    xy_two_qubit_gates = k_pairs * 2 * depth
    if include_agp:
        xy_two_qubit_gates *= 2

    # IonQ Trapped Ion: 0 routing SWAPs due to all-to-all connectivity
    ionq_swaps = 0
    ionq_depth = depth * (4 if not include_agp else 8)

    # IBM Heavy-Hex: linear/sparse chain requires SWAP network: O(n^2) SWAPs
    ibm_swaps = max(1, int(k_pairs - (n_qubits - 1)))
    ibm_two_qubit_gates = xy_two_qubit_gates + 3 * ibm_swaps
    ibm_depth = ionq_depth + 3 * ibm_swaps

    return {
        "n_qubits": n_qubits,
        "circuit_depth_ideal": ionq_depth,
        "two_qubit_interactions": k_pairs,
        "ionq_trapped_ion": {
            "routing_swaps": ionq_swaps,
            "two_qubit_cx_gates": xy_two_qubit_gates,
            "circuit_depth": ionq_depth,
            "topology": "All-to-all K_n",
        },
        "ibm_heavy_hex": {
            "routing_swaps": ibm_swaps,
            "two_qubit_cx_gates": ibm_two_qubit_gates,
            "circuit_depth": ibm_depth,
            "topology": "Sparse Nearest-Neighbor",
        }
    }
