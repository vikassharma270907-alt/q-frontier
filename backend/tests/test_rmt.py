"""
Unit Tests for Stage 1: RMT Clustering & Spectral Denoising
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


def test_synthetic_data_generation():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    assert len(df) == 180
    assert list(df.columns) == DEFAULT_TICKERS
    assert not df.isnull().values.any()


def test_expected_returns_and_covariance():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    mu, cov, tickers = compute_expected_returns_and_covariance(df)
    
    assert len(mu) == len(DEFAULT_TICKERS)
    assert cov.shape == (len(DEFAULT_TICKERS), len(DEFAULT_TICKERS))
    assert tickers == DEFAULT_TICKERS
    # Positive semi-definiteness
    eigvals = np.linalg.eigvalsh(cov)
    assert np.all(eigvals >= -1e-8)


def test_marchenko_pastur_denoising():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    mu, cov, tickers = compute_expected_returns_and_covariance(df)
    
    denoised_cov, denoised_corr, lambda_plus = marchenko_pastur_denoise(
        cov, t_samples=180, n_assets=len(tickers)
    )
    
    assert denoised_cov.shape == cov.shape
    assert denoised_corr.shape == cov.shape
    assert lambda_plus > 0.0
    # Diagonal of correlation matrix should be exactly 1
    assert np.allclose(np.diag(denoised_corr), 1.0, atol=1e-5)
    # Denoised covariance must remain positive semi-definite
    denoised_eigs = np.linalg.eigvalsh(denoised_cov)
    assert np.all(denoised_eigs >= -1e-8)


def test_get_clusters_partitioning():
    df = generate_synthetic_nasdaq_data(DEFAULT_TICKERS, days=180)
    mu, cov, tickers = compute_expected_returns_and_covariance(df)
    _, denoised_corr, _ = marchenko_pastur_denoise(cov, t_samples=180, n_assets=len(tickers))
    
    clusters = get_clusters(denoised_corr, tickers, max_cluster_size=4)
    assert len(clusters) == 3  # 12 assets divided into max 4 per cluster = 3 clusters
    
    all_indices = []
    for c in clusters:
        assert c["size"] <= 4
        all_indices.extend(c["indices"])
        
    assert sorted(all_indices) == list(range(12))
