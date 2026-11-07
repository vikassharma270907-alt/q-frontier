"""
Return calculations and expected return estimators for equity universes.
"""

from __future__ import annotations
from typing import Tuple, List
import numpy as np
import pandas as pd


def compute_returns(
    prices: pd.DataFrame,
    method: str = "simple"
) -> pd.DataFrame:
    """
    Computes periodic return series from price levels.
    method: 'simple' for pct_change, 'log' for natural log difference.
    """
    if method == "log":
        return np.log(np.maximum(prices, 1e-8)).diff().dropna()
    return prices.pct_change().dropna()


def compute_expected_returns(
    returns: pd.DataFrame,
    annualization_factor: float = 252.0
) -> Tuple[np.ndarray, List[str]]:
    """
    Computes annualized arithmetic mean returns for assets:
    mu = mean(returns) * annualization_factor.
    """
    tickers = list(returns.columns)
    mu = returns.mean().values * annualization_factor
    return mu, tickers
