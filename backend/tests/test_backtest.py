"""
Unit Tests for Stage 4: SLSQP Allocation, Walk-Forward Backtesting & Hardware Benchmarks
"""

import numpy as np
import pandas as pd
import pytest
from app.rmt_clustering import DEFAULT_TICKERS, generate_synthetic_nasdaq_data
from app.slsqp_backtest import optimize_continuous_weights_slsqp, run_walk_forward_backtest
from app.hardware_benchmarks import generate_hardware_comparison, generate_sandia_volumetric_grid


def test_slsqp_optimization():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    returns = df.pct_change().dropna()
    mu = returns.mean().values * 252.0
    cov = returns.cov().values * 252.0
    
    selected_indices = [0, 2, 4, 6, 8, 10]
    weights, sharpe = optimize_continuous_weights_slsqp(selected_indices, mu, cov)
    
    # 1. Weights sum to 1.0
    assert np.isclose(np.sum(weights), 1.0, atol=1e-5)
    # 2. Non-selected assets have 0 weight
    for i in range(len(DEFAULT_TICKERS)):
        if i not in selected_indices:
            assert np.isclose(weights[i], 0.0)
    # 3. Sharpe ratio is positive
    assert sharpe > 0.0


def test_walk_forward_backtest():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=120)
    selected_indices = [0, 2, 4, 6, 8, 10]
    
    res = run_walk_forward_backtest(df, selected_indices, transaction_cost_bps=5.0)
    
    assert res["final_portfolio_value"] > 50.0
    assert "equity_curve" in res
    assert len(res["equity_curve"]) > 0
    assert res["transaction_costs_paid"] >= 0.0


def test_hardware_benchmarks_and_sandia_grid():
    hw = generate_hardware_comparison(n_qubits=4)
    assert hw["ionq_trapped_ion"]["routing_swaps"] == 0
    assert hw["ibm_heavy_hex"]["routing_swaps"] >= 1
    
    grid = generate_sandia_volumetric_grid()
    assert len(grid) == 20  # 4 widths * 5 depths
    for cell in grid:
        assert 0.0 <= cell["approximation_ratio"] <= 1.0
        assert 0.0 <= cell["reachable_quality_qr"] <= 1.0
