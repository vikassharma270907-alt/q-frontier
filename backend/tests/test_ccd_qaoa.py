"""
Unit Tests for Stage 3: CCD-QAOA Solver & Exact Commutation Properties
"""

import numpy as np
import pytest
from app.ccd_qaoa_solver import (
    CCDQAOASolver,
    prepare_dicke_statevector,
    build_xy_mixer_matrix,
    create_n_qubit_operator,
    Z,
)


def test_dicke_state_properties():
    n_qubits = 4
    k = 2
    state = prepare_dicke_statevector(n_qubits, k)
    
    # Unit norm
    assert np.isclose(np.linalg.norm(state), 1.0)
    
    # Nonzero amplitudes only on Hamming weight k
    for i, amp in enumerate(state):
        w = bin(i)[2:].zfill(n_qubits).count("1")
        if w == k:
            assert np.isclose(np.abs(amp), 1.0 / np.sqrt(6))
        else:
            assert np.isclose(amp, 0.0)

    # Boundary checks: invalid k_weight raises ValueError
    with pytest.raises(ValueError):
        prepare_dicke_statevector(4, 5)
    with pytest.raises(ValueError):
        prepare_dicke_statevector(4, -1)


def test_xy_mixer_commutation():
    """Verify [H_M^{XY}, sum_i Z_i] = 0 strictly preserving Hamming weight."""
    n_qubits = 4
    h_xy = build_xy_mixer_matrix(n_qubits)
    
    # Construct sum_i Z_i
    dim = 2 ** n_qubits
    z_total = np.zeros((dim, dim), dtype=complex)
    for i in range(n_qubits):
        z_total += create_n_qubit_operator({i: Z}, n_qubits)
        
    commutator = h_xy @ z_total - z_total @ h_xy
    norm_comm = np.linalg.norm(commutator)
    assert np.isclose(norm_comm, 0.0, atol=1e-10)


def test_ccd_qaoa_solve():
    solver = CCDQAOASolver(n_qubits=4, k_cardinality=2)
    
    np.random.seed(42)
    cov_sub = np.array([
        [0.08, 0.03, 0.02, 0.01],
        [0.03, 0.09, 0.04, 0.02],
        [0.02, 0.04, 0.07, 0.03],
        [0.01, 0.02, 0.03, 0.06]
    ])
    mu_sub = np.array([0.18, 0.22, 0.15, 0.12])
    
    res = solver.solve(cov_sub, mu_sub, q_risk=0.6, depth=1)
    
    # 1. Cardinality check: sum(optimal_selection) == 2
    assert sum(res["optimal_selection"]) == 2
    
    # 2. Feasibility check: CCD-QAOA has 100% feasibility
    assert np.isclose(res["ccd_qaoa"]["feasibility"], 1.0, atol=1e-5)
    assert np.isclose(res["xy_qaoa"]["feasibility"], 1.0, atol=1e-5)
    
    # 3. Penalty-QAOA exhibits shot leakage (< 100%)
    assert res["penalty_qaoa"]["feasibility"] < 0.95
    
    # 4. CCD-QAOA achieves high Approximation Ratio at p=1
    assert res["ccd_qaoa"]["approximation_ratio"] > 0.85
    # Near-degenerate optimal cluster states capture the majority probability mass
    assert res["ccd_qaoa"]["optimal_probability"] >= 0.25
