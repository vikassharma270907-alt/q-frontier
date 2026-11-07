"""
Unit tests comparing Exact, Heuristic, and Quantum Simulator Solvers.
"""

import pytest
import numpy as np

from app.solvers.exact import ExactEnumerationSolver
from app.solvers.annealing import SimulatedAnnealingSolver
from app.solvers.xy_qaoa import XYQAOASolver
from app.solvers.penalty_qaoa import PenaltyQAOASolver
from app.solvers.agp_experiment import CounterdiabaticQAOASolver
from app.solvers.gnn_mixer import GNNSparseXYQAOASolver, compute_gnn_sparse_edges


@pytest.fixture
def toy_problem():
    cov = np.array([
        [0.08, 0.03, 0.02, 0.01],
        [0.03, 0.09, 0.04, 0.02],
        [0.02, 0.04, 0.07, 0.03],
        [0.01, 0.02, 0.03, 0.06]
    ])
    mu = np.array([0.18, 0.22, 0.15, 0.12])
    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]
    return cov, mu, tickers


def test_exact_solver(toy_problem):
    cov, mu, tickers = toy_problem
    solver = ExactEnumerationSolver()
    res = solver.solve(cov, mu, k_cardinality=2, tickers=tickers, lambda_risk=0.5)

    assert res.solver_type == "CLASSICAL_EXACT"
    assert len(res.selected_indices) == 2
    assert res.is_feasible is True
    assert res.feasibility_rate == 1.0
    assert res.approximation_ratio == 1.0
    assert res.optimal_probability == 1.0


def test_simulated_annealing_solver(toy_problem):
    cov, mu, tickers = toy_problem
    exact_res = ExactEnumerationSolver().solve(cov, mu, k_cardinality=2, tickers=tickers)

    sa_solver = SimulatedAnnealingSolver(max_iterations=500)
    res = sa_solver.solve(
        cov, mu, k_cardinality=2, tickers=tickers,
        seed=42,
        ground_truth_min=exact_res.objective_value,
        ground_truth_max=exact_res.metadata["e_max"]
    )

    assert res.solver_type == "CLASSICAL_HEURISTIC"
    assert len(res.selected_indices) == 2
    assert res.feasibility_rate == 1.0
    assert res.approximation_ratio >= 0.80


def test_xy_and_ccd_qaoa_solvers(toy_problem):
    cov, mu, tickers = toy_problem
    exact_res = ExactEnumerationSolver().solve(cov, mu, k_cardinality=2, tickers=tickers)

    # XY-QAOA
    xy_solver = XYQAOASolver()
    xy_res = xy_solver.solve(
        cov, mu, k_cardinality=2, tickers=tickers, depth=1,
        ground_truth_min=exact_res.objective_value,
        ground_truth_max=exact_res.metadata["e_max"]
    )
    assert xy_res.solver_type == "SIMULATED_QUANTUM"
    assert xy_res.feasibility_rate == 1.0
    assert xy_res.approximation_ratio >= 0.60

    # CCD-QAOA (Counterdiabatic)
    ccd_solver = CounterdiabaticQAOASolver()
    ccd_res = ccd_solver.solve(
        cov, mu, k_cardinality=2, tickers=tickers, depth=1,
        ground_truth_min=exact_res.objective_value,
        ground_truth_max=exact_res.metadata["e_max"]
    )
    assert ccd_res.solver_type == "SIMULATED_QUANTUM"
    assert ccd_res.feasibility_rate == 1.0
    assert ccd_res.approximation_ratio >= 0.80
    # CCD-QAOA out-performs standard XY-QAOA at shallow depth p=1
    assert ccd_res.approximation_ratio > xy_res.approximation_ratio


def test_penalty_qaoa_shot_leakage(toy_problem):
    cov, mu, tickers = toy_problem
    pen_solver = PenaltyQAOASolver()
    pen_res = pen_solver.solve(cov, mu, k_cardinality=2, tickers=tickers, depth=1)

    assert pen_res.solver_type == "SIMULATED_QUANTUM"
    # Unconstrained mixer exhibits shot leakage (feasibility < 100%)
    assert pen_res.feasibility_rate < 0.95
    assert pen_res.metadata["shot_leakage_pct"] > 5.0


def test_gnn_sparse_xy_qaoa_solver(toy_problem):
    """Verify GNN sparsified XY mixer preserves 100% feasibility and cuts gate count."""
    cov, mu, tickers = toy_problem
    exact_res = ExactEnumerationSolver().solve(cov, mu, k_cardinality=2, tickers=tickers)

    gnn_solver = GNNSparseXYQAOASolver()
    res = gnn_solver.solve(
        cov, mu, k_cardinality=2, tickers=tickers, depth=1,
        ground_truth_min=exact_res.objective_value,
        ground_truth_max=exact_res.metadata["e_max"]
    )

    assert res.solver_type == "SIMULATED_QUANTUM"
    assert res.feasibility_rate == pytest.approx(1.0)
    assert res.metadata["subspace_preserved"] is True
    assert res.metadata["commutation_error"] < 1e-10
    assert res.metadata["cnot_reduction_pct"] > 0
    assert res.approximation_ratio >= 0.60

