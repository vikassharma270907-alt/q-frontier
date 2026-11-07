"""
Unit Tests for Context-Aware Folding (CAF) Coordination
"""

import numpy as np
import pytest
from app.rmt_clustering import (
    DEFAULT_TICKERS,
    generate_synthetic_nasdaq_data,
    compute_expected_returns_and_covariance,
    marchenko_pastur_denoise,
    get_clusters,
)
from app.caf_coordinator import CAFCoordinator


def test_caf_coordination_and_monotonicity():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    mu, cov, tickers = compute_expected_returns_and_covariance(df)
    denoised_cov, denoised_corr, _ = marchenko_pastur_denoise(cov, 180, len(tickers))
    clusters = get_clusters(denoised_corr, tickers, max_cluster_size=4)
    
    coordinator = CAFCoordinator(
        denoised_cov=denoised_cov,
        expected_returns=mu,
        clusters=clusters,
        q_risk=0.6,
        continuity_bonus=0.05
    )
    
    res = coordinator.run_caf_coordination(k_per_cluster=2, max_outer_iterations=2, depth=1)
    
    # 1. Total assets selected = 3 clusters * 2 = 6 assets
    assert len(res["selected_indices"]) == 6
    
    # 2. Monotonic energy descent: CAF energy must be <= static energy
    assert res["caf_energy"] <= res["static_energy"] + 1e-6
    
    # 3. Energy trajectory is non-increasing
    traj = res["energy_trajectory"]
    for i in range(1, len(traj)):
        assert traj[i] <= traj[i-1] + 1e-6
