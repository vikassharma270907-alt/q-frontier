"""
Deterministic synthetic price history generators with fixed seeds for offline and auditable research.
"""

from __future__ import annotations
from typing import List, Dict, Optional
import numpy as np
import pandas as pd

PRESET_UNIVERSES: Dict[str, List[str]] = {
    "TECH_4": ["AAPL", "MSFT", "NVDA", "GOOGL"],
    "NASDAQ_8": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO"],
    "NASDAQ_12": [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META",
        "TSLA", "AVGO", "COST", "CSCO", "NFLX", "AMD"
    ],
}


def generate_synthetic_prices(
    tickers: Optional[List[str]] = None,
    days: int = 180,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic, reproducible synthetic equity price paths using a 3-factor market model:
      - Broad Market factor (beta_m)
      - Tech factor (beta_t)
      - Semiconductor factor (beta_s)
    Uses a fixed seed to guarantee offline reproducibility.
    """
    if tickers is None:
        tickers = PRESET_UNIVERSES["NASDAQ_12"]

    rng = np.random.default_rng(seed)
    dates = pd.date_range(end="2026-11-06", periods=days, freq="B")
    n = len(tickers)

    f_market = rng.normal(0.0006, 0.012, days)
    f_tech = rng.normal(0.0004, 0.015, days)
    f_semi = rng.normal(0.0005, 0.020, days)

    prices_dict: Dict[str, np.ndarray] = {}
    for i, t in enumerate(tickers):
        beta_m = 0.8 + 0.5 * (i % 3) / 2.0
        beta_t = 0.4 + 0.6 * ((i + 1) % 4) / 3.0
        beta_s = 0.5 if any(x in t for x in ["NVDA", "AMD", "AVGO", "MU", "INTC"]) else 0.1
        noise = rng.normal(0.0, 0.01, days)

        daily_ret = beta_m * f_market + beta_t * f_tech + beta_s * f_semi + noise
        price_series = 100.0 * np.exp(np.cumsum(daily_ret))
        prices_dict[t] = price_series

    return pd.DataFrame(prices_dict, index=dates)
