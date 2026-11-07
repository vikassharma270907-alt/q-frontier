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
    "CRISIS_2026": [
        "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META",
        "TSLA", "AVGO", "COST", "CSCO", "NFLX", "AMD"
    ],
    "FLASH_CRASH_8": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO"],
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


def generate_crisis_prices(
    scenario: str = "CRISIS_2026_LIQUIDITY",
    tickers: Optional[List[str]] = None,
    days: int = 180,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic non-stationary financial stress scenarios with regime switching,
    volatility clustering, and correlation breakdown (tail contagion).

    Scenarios:
      - 'CRISIS_2026_LIQUIDITY': Calm regime (t=0..120), systemic liquidity crunch (t=120..155,
        rho -> 0.85, 3x vol, fat tails), followed by high-dispersion recovery.
      - 'CRISIS_FLASH_CRASH': Sudden acute liquidity vacuum with -15% intraday drops.
      - 'CRISIS_TECH_ROTATION': High dispersion where tech drops while defensive staples rally.
    """
    if tickers is None:
        tickers = PRESET_UNIVERSES["CRISIS_2026"]

    rng = np.random.default_rng(seed)
    dates = pd.date_range(end="2026-11-06", periods=days, freq="B")
    n = len(tickers)

    # Base common shock factor and idiosyncratic noise
    f_common = rng.normal(0.0004, 0.010, days)
    regime_multiplier = np.ones(days)
    correlation_surge = np.zeros(days)

    if scenario == "CRISIS_2026_LIQUIDITY":
        # Sudden systemic shock starting around day 120
        shock_start = int(days * 0.65)
        shock_end = int(days * 0.85)
        regime_multiplier[shock_start:shock_end] = 3.5
        correlation_surge[shock_start:shock_end] = 0.80
        # Negative drift during crisis
        f_common[shock_start:shock_end] -= 0.022
    elif scenario == "CRISIS_FLASH_CRASH":
        crash_day = int(days * 0.75)
        regime_multiplier[crash_day : crash_day + 5] = 5.0
        correlation_surge[crash_day : crash_day + 5] = 0.90
        f_common[crash_day : crash_day + 3] -= 0.045
    elif scenario == "CRISIS_TECH_ROTATION":
        rot_start = int(days * 0.60)
        regime_multiplier[rot_start:] = 2.0

    prices_dict: Dict[str, np.ndarray] = {}
    for i, t in enumerate(tickers):
        is_defensive = any(x in t for x in ["COST", "CSCO", "JNJ", "PG", "WMT"])
        base_beta = 0.9 + 0.3 * (i % 3)
        idiosyncratic = rng.normal(0.0, 0.012, days)

        daily_ret = np.zeros(days)
        for d in range(days):
            vol = regime_multiplier[d]
            c_surge = correlation_surge[d]

            if scenario == "CRISIS_TECH_ROTATION" and d >= int(days * 0.60):
                drift = 0.008 if is_defensive else -0.015
                daily_ret[d] = drift + (0.5 * f_common[d] + 0.5 * idiosyncratic[d]) * vol
            else:
                # Correlation breakdown: all equities move with common factor during panic
                market_weight = (1.0 - c_surge) * base_beta + c_surge * 1.8
                daily_ret[d] = market_weight * f_common[d] * vol + (1.0 - c_surge) * idiosyncratic[d] * np.sqrt(vol)

        price_series = 100.0 * np.exp(np.cumsum(daily_ret))
        prices_dict[t] = price_series

    return pd.DataFrame(prices_dict, index=dates)
