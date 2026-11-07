"""
Unit tests for finance core: returns, covariance estimators, objective correctness, and brute-force equivalence.
"""

import pytest
import numpy as np
import pandas as pd

from app.finance.returns import compute_returns, compute_expected_returns
from app.finance.covariance import (
    compute_sample_covariance,
    compute_ledoit_wolf_covariance,
    compute_rmt_marchenko_pastur_covariance,
    covariance_to_correlation,
)
from app.finance.objective import (
    evaluate_selection_objective,
    check_cardinality_feasibility,
    compute_all_bitstring_energies,
)
from app.data.synthetic import generate_synthetic_prices, PRESET_UNIVERSES


def test_returns_and_covariance_properties():
    """Verify returns, covariance symmetry, and positive semi-definiteness."""
    prices = generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_8"], days=90, seed=123)
    returns = compute_returns(prices, method="simple")
    mu, tickers = compute_expected_returns(returns)

    assert len(mu) == 8
    assert len(tickers) == 8

    cov_sample = compute_sample_covariance(returns)
    assert cov_sample.shape == (8, 8)
    assert np.allclose(cov_sample, cov_sample.T)
    eigs_sample = np.linalg.eigvalsh(cov_sample)
    assert np.all(eigs_sample >= -1e-8)

    cov_lw, shrinkage = compute_ledoit_wolf_covariance(returns)
    assert cov_lw.shape == (8, 8)
    assert 0.0 <= shrinkage <= 1.0
    assert np.allclose(cov_lw, cov_lw.T)
    eigs_lw = np.linalg.eigvalsh(cov_lw)
    assert np.all(eigs_lw >= -1e-8)

    cov_rmt, corr_rmt, lambda_plus = compute_rmt_marchenko_pastur_covariance(
        cov_sample, t_samples=len(returns), n_assets=8
    )
    assert cov_rmt.shape == (8, 8)
    assert np.allclose(np.diag(corr_rmt), 1.0, atol=1e-5)
    assert lambda_plus > 0.0


def test_objective_matches_brute_force_toy_instances():
    """
    Verify binary quadratic objective matches brute-force enumeration across 20 random instances.
    Mandatory acceptance test from Master Prompt Phase 0.
    """
    rng = np.random.default_rng(42)

    for trial in range(20):
        n = 5
        k = 2
        # Generate random symmetric positive definite covariance matrix
        a = rng.normal(0, 1, (n, n))
        cov = a.T @ a + np.eye(n) * 0.1
        mu = rng.normal(0.1, 0.05, n)
        lambda_risk = float(rng.uniform(0.1, 0.9))

        energies, bitstrings = compute_all_bitstring_energies(cov, mu, lambda_risk=lambda_risk)

        # Brute-force check all Hamming-weight-K bitstrings
        min_feasible_energy = float("inf")
        best_vec = None
        for i, b_str in enumerate(bitstrings):
            if b_str.count("1") == k:
                vec = np.array([int(c) for c in b_str], dtype=float)
                # Compute manual objective
                manual_obj = lambda_risk * (vec @ cov @ vec) - (1.0 - lambda_risk) * np.dot(mu, vec)
                assert np.isclose(energies[i], manual_obj, atol=1e-8)
                if manual_obj < min_feasible_energy:
                    min_feasible_energy = manual_obj
                    best_vec = vec

        assert best_vec is not None
        assert check_cardinality_feasibility(best_vec, k) is True
