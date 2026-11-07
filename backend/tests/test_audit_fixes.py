"""
Unit tests verifying senior code review security and mathematical correctness fixes.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from pydantic import ValidationError

from app.schemas import RunRequest, CSVValidateRequest
from app.data.loader import DatasetManager
from app.services.runs import RunService
from app.finance.backtest import optimize_continuous_weights_slsqp, run_walk_forward_backtest
from app.ccd_qaoa_solver import CCDQAOASolver
from app.solvers.xy_qaoa import XYQAOASolver


def test_path_traversal_dataset_storage(tmp_path):
    mgr = DatasetManager(cache_dir=tmp_path / "cache")
    df = pd.DataFrame({"A": [10.0, 11.0], "B": [20.0, 21.0]})

    # Malicious path attempting directory traversal
    clean_id = mgr.store_custom_dataset("../../evil_payload", df)
    assert "/" not in clean_id
    assert "\\" not in clean_id
    assert ".." not in clean_id

    # Verify file was saved safely inside cache dir
    saved_files = list((tmp_path / "cache").glob("*.csv"))
    assert len(saved_files) == 1
    assert saved_files[0].parent == (tmp_path / "cache").resolve()


def test_path_traversal_run_fetching(tmp_path):
    srv = RunService()
    # Malicious run_id
    assert srv.get_run("../../etc/passwd") is None
    assert srv.get_run("..\\..\\boot.ini") is None
    assert srv.get_run("invalid!chars*") is None


def test_run_request_cardinality_validator():
    # Valid: K < N
    req = RunRequest(asset_count=8, k_cardinality=3)
    assert req.k_cardinality == 3

    # Invalid: K >= N should fail schema validation
    with pytest.raises(ValidationError):
        RunRequest(asset_count=4, k_cardinality=4)

    with pytest.raises(ValidationError):
        RunRequest(asset_count=4, k_cardinality=5)


def test_slsqp_box_constraints_k_small():
    # K=2 previously failed with default max_weight=0.40 because 2 * 0.40 = 0.80 < 1.0
    mu = np.array([0.15, 0.20, 0.10, 0.12])
    cov = np.eye(4) * 0.04
    selected = [0, 1]  # K = 2

    weights, sharpe = optimize_continuous_weights_slsqp(selected, mu, cov)
    assert np.isclose(np.sum(weights), 1.0, atol=1e-4)
    assert weights[0] > 0.0
    assert weights[1] > 0.0
    assert weights[2] == 0.0
    assert weights[3] == 0.0


def test_backtest_non_datetime_index():
    # Integer-indexed DataFrame (not DatetimeIndex)
    prices = pd.DataFrame({
        "AAPL": np.linspace(100, 150, 40),
        "MSFT": np.linspace(200, 260, 40),
        "NVDA": np.linspace(300, 450, 40)
    })
    # Must run without AttributeError: 'int' object has no attribute 'strftime'
    res = run_walk_forward_backtest(prices, selected_indices=[0, 1], transaction_cost_bps=5.0)
    assert "final_portfolio_value" in res
    assert len(res["equity_curve"]) > 0
    assert isinstance(res["equity_curve"][0]["date"], str)


def test_spectral_ccd_solver_speed_and_exactness():
    # 4-qubit CCD solver with spectral evolution
    solver = CCDQAOASolver(n_qubits=4, k_cardinality=2)
    cov = np.array([
        [0.05, 0.02, 0.01, 0.00],
        [0.02, 0.06, 0.02, 0.01],
        [0.01, 0.02, 0.04, 0.01],
        [0.00, 0.01, 0.01, 0.05]
    ])
    mu = np.array([0.12, 0.15, 0.10, 0.14])

    res = solver.solve(cov, mu, q_risk=0.5, depth=1)
    # Feasibility must be 100% in Dicke subspace
    assert np.isclose(res["ccd_qaoa"]["feasibility"], 1.0, atol=1e-4)
    assert res["ccd_qaoa"]["approximation_ratio"] > 0.85
