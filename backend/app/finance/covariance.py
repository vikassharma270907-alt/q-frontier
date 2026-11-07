"""
Covariance matrix estimators: Sample Covariance, Ledoit-Wolf Shrinkage,
and Random Matrix Theory (RMT) Marchenko-Pastur spectral filtering.
"""

from __future__ import annotations
from typing import Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf


def compute_sample_covariance(
    returns: pd.DataFrame,
    annualization_factor: float = 252.0
) -> np.ndarray:
    """Computes standard sample covariance scaled to annual terms."""
    cov = returns.cov().values * annualization_factor
    # Ensure exact numerical symmetry
    cov = 0.5 * (cov + cov.T)
    return cov


def compute_ledoit_wolf_covariance(
    returns: pd.DataFrame,
    annualization_factor: float = 252.0
) -> Tuple[np.ndarray, float]:
    """
    Computes Ledoit-Wolf analytical shrinkage covariance towards constant correlation target.
    Returns: (cov_matrix, shrinkage_intensity)
    """
    lw = LedoitWolf()
    lw.fit(returns.values)
    cov = lw.covariance_ * annualization_factor
    cov = 0.5 * (cov + cov.T)
    shrinkage = float(lw.shrinkage_)
    return cov, shrinkage


def compute_rmt_marchenko_pastur_covariance(
    cov_matrix: np.ndarray,
    t_samples: int,
    n_assets: int
) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Applies Random Matrix Theory (RMT) Marchenko-Pastur spectral filtering.
    Separates eigenvalues into empirical noise bulk (<= lambda_+) and true market modes.
    Eigenvalues within the noise bulk are replaced with their trace-preserving average.
    Returns: (denoised_cov, denoised_corr, lambda_plus)
    """
    std = np.sqrt(np.diag(cov_matrix))
    inv_std = 1.0 / np.where(std == 0, 1e-8, std)
    corr = inv_std[:, None] * cov_matrix * inv_std[None, :]
    np.fill_diagonal(corr, 1.0)

    eigvals, eigvecs = np.linalg.eigh(corr)
    # Sort descending
    sort_idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[sort_idx]
    eigvecs = eigvecs[:, sort_idx]

    q_ratio = float(t_samples) / float(n_assets)
    sigma_sq = max(1e-6, 1.0 - (eigvals[0] / float(n_assets)))
    lambda_plus = float(sigma_sq * ((1.0 + np.sqrt(1.0 / q_ratio)) ** 2))

    noise_mask = eigvals <= lambda_plus
    if np.any(noise_mask):
        mean_noise = float(np.mean(eigvals[noise_mask]))
        denoised_eigvals = np.where(noise_mask, mean_noise, eigvals)
    else:
        denoised_eigvals = eigvals.copy()

    denoised_corr = eigvecs @ np.diag(denoised_eigvals) @ eigvecs.T
    d = np.sqrt(np.diag(denoised_corr))
    denoised_corr = denoised_corr / (d[:, None] @ d[None, :])
    np.fill_diagonal(denoised_corr, 1.0)

    denoised_cov = (std[:, None] * denoised_corr) * std[None, :]
    denoised_cov = 0.5 * (denoised_cov + denoised_cov.T)

    return denoised_cov, denoised_corr, lambda_plus


def covariance_to_correlation(cov: np.ndarray) -> np.ndarray:
    """Extracts symmetric correlation matrix from covariance matrix."""
    std = np.sqrt(np.diag(cov))
    inv_std = 1.0 / np.where(std == 0, 1e-8, std)
    corr = inv_std[:, None] * cov * inv_std[None, :]
    np.fill_diagonal(corr, 1.0)
    return corr
