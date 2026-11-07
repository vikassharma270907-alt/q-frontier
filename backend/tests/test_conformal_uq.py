"""
Unit tests for Conformal Prediction & Quantum Uncertainty Quantification.
"""

import pytest
import numpy as np
import pandas as pd

from app.metrics.conformal import compute_conformal_portfolio_bounds


def test_conformal_portfolio_bounds_ordering():
    """Verify calibrated lower bound <= point estimate <= upper bound."""
    rng = np.random.default_rng(42)
    days = 120
    returns_matrix = rng.normal(0.0005, 0.015, (days, 4))
    returns_df = pd.DataFrame(returns_matrix, columns=["A", "B", "C", "D"])
    weights = np.array([0.5, 0.5])
    selected_indices = [0, 1]

    bounds = compute_conformal_portfolio_bounds(
        returns_df=returns_df,
        weights=weights,
        selected_indices=selected_indices,
        shots=1024,
        alpha=0.05
    )

    ret_low, ret_high = bounds["conformal_return_interval_pct"]
    assert ret_low <= bounds["expected_return_pct"] <= ret_high, "Return point estimate must lie within conformal bounds"

    vol_low, vol_high = bounds["conformal_volatility_interval_pct"]
    assert vol_low <= bounds["expected_volatility_pct"] <= vol_high, "Volatility point estimate must lie within conformal bounds"

    sharpe_low, sharpe_high = bounds["conformal_sharpe_interval"]
    assert sharpe_low <= bounds["sharpe_ratio_point"] <= sharpe_high, "Sharpe point estimate must lie within conformal bounds"

    assert bounds["confidence_level"] == 0.95
    assert bounds["quantum_shots_evaluated"] == 1024


def test_conformal_shot_noise_scaling():
    """Higher shot count should reduce quantum shot uncertainty margin."""
    rng = np.random.default_rng(101)
    returns_matrix = rng.normal(0.0005, 0.015, (100, 3))
    returns_df = pd.DataFrame(returns_matrix, columns=["A", "B", "C"])

    bounds_low_shots = compute_conformal_portfolio_bounds(returns_df, np.array([1.0]), [0], shots=256)
    bounds_high_shots = compute_conformal_portfolio_bounds(returns_df, np.array([1.0]), [0], shots=8192)

    assert bounds_high_shots["quantum_shot_noise_bps"] < bounds_low_shots["quantum_shot_noise_bps"]
