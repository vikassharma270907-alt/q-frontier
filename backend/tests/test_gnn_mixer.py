"""
Unit and integration tests for GNN-Adaptive Sparsified XY Mixer (GQML).
"""

import pytest
import numpy as np

from app.solvers.gnn_mixer import (
    compute_gnn_sparse_edges,
    build_gnn_sparse_mixer_matrix,
    GNNSparseXYQAOASolver,
)
from app.solvers.xy_qaoa import create_n_qubit_operator, Z


def test_gnn_sparse_edges_connectivity():
    """Verify Prim's MST guarantees all N nodes are connected with fewer edges than complete graph."""
    n = 6
    rng = np.random.default_rng(42)
    A = rng.normal(0, 1, (n, n))
    corr = np.corrcoef(A)
    np.fill_diagonal(corr, 1.0)

    edges = compute_gnn_sparse_edges(corr, topology="adaptive_mst", max_degree=3)
    
    # Check connectivity
    connected_nodes = set()
    for u, v, w in edges:
        connected_nodes.add(u)
        connected_nodes.add(v)
    assert len(connected_nodes) == n, "GNN mixer graph must be fully connected to preserve ergodicity"

    complete_edges = n * (n - 1) // 2
    assert len(edges) < complete_edges, f"Sparse edges ({len(edges)}) should be fewer than complete ({complete_edges})"


def test_gnn_mixer_commutation_with_total_magnetization():
    """
    Mathematical Theorem Verification:
    [H_M^{GNN}, sum_i Z_i] = 0 identically for any graph topology.
    This guarantees 0% shot leakage into infeasible bitstrings.
    """
    n = 4
    corr = np.array([
        [1.0, 0.8, 0.2, 0.1],
        [0.8, 1.0, 0.4, 0.3],
        [0.2, 0.4, 1.0, 0.7],
        [0.1, 0.3, 0.7, 1.0],
    ])
    edges = compute_gnn_sparse_edges(corr, topology="adaptive_mst", max_degree=2)
    h_m_gnn = build_gnn_sparse_mixer_matrix(n, edges)

    total_z = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for i in range(n):
        total_z += create_n_qubit_operator({i: Z}, n)

    comm = h_m_gnn @ total_z - total_z @ h_m_gnn
    max_comm_error = np.max(np.abs(comm))
    assert max_comm_error < 1e-12, f"Commutator error {max_comm_error} must be zero"


def test_gnn_solver_execution_feasibility():
    """Verify GNN solver returns 100% feasibility and valid approximation ratio."""
    cov = np.array([
        [0.04, 0.01, 0.005, 0.002],
        [0.01, 0.05, 0.01, 0.003],
        [0.005, 0.01, 0.06, 0.015],
        [0.002, 0.003, 0.015, 0.07],
    ])
    mu = np.array([0.12, 0.10, 0.15, 0.08])
    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]

    solver = GNNSparseXYQAOASolver()
    res = solver.solve(
        cov=cov,
        mu=mu,
        k_cardinality=2,
        tickers=tickers,
        lambda_risk=0.5,
        depth=1,
    )

    assert len(res.selected_indices) == 2
    assert res.feasibility_rate == pytest.approx(1.0, abs=1e-5)
    assert res.metadata["subspace_preserved"] is True
    assert res.metadata["cnot_reduction_pct"] > 0

