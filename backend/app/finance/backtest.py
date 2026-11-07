"""
Continuous SLSQP weight optimization and chronological walk-forward portfolio backtesting.
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def optimize_continuous_weights_slsqp(
    selected_indices: List[int],
    expected_returns: np.ndarray,
    covariance_matrix: np.ndarray,
    risk_free_rate: float = 0.04,
    min_weight: float = 0.02,
    max_weight: float = 0.40
) -> Tuple[np.ndarray, float]:
    """
    Optimizes continuous portfolio weights for selected assets using SLSQP.
    Maximizes Sharpe Ratio subject to full investment and min/max weight bounds.
    Returns: (optimal_weights_full_N, optimized_sharpe_ratio)
    """
    n_total = len(expected_returns)
    k = len(selected_indices)
    weights_full = np.zeros(n_total, dtype=float)

    if k == 0:
        return weights_full, 0.0

    mu_s = expected_returns[selected_indices]
    cov_s = covariance_matrix[np.ix_(selected_indices, selected_indices)]

    def negative_sharpe(w):
        port_ret = np.dot(w, mu_s)
        port_var = w @ cov_s @ w
        port_vol = np.sqrt(max(port_var, 1e-8))
        return -(port_ret - risk_free_rate) / port_vol

    init_w = np.ones(k) / float(k)
    effective_min = min(min_weight, 1.0 / k)
    effective_max = max(max_weight, 1.0 / k)
    bounds = [(effective_min, effective_max) for _ in range(k)]
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]

    res = minimize(
        negative_sharpe,
        init_w,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 100}
    )

    opt_w = res.x if res.success else init_w
    opt_w = opt_w / np.sum(opt_w)

    for local_i, global_i in enumerate(selected_indices):
        weights_full[global_i] = opt_w[local_i]

    port_ret = float(np.dot(weights_full, expected_returns))
    port_vol = float(np.sqrt(weights_full @ covariance_matrix @ weights_full))
    sharpe = float((port_ret - risk_free_rate) / max(port_vol, 1e-6))

    return weights_full, sharpe


def run_walk_forward_backtest(
    prices: pd.DataFrame,
    selected_indices: List[int],
    transaction_cost_bps: float = 5.0,
    rebalance_freq_days: int = 21
) -> Dict[str, Any]:
    """
    Chronological out-of-sample walk-forward historical simulation evaluating portfolio value
    net of transaction costs and rebalancing turnover.
    """
    daily_returns = prices.pct_change().dropna()
    dates = daily_returns.index
    n_days = len(daily_returns)
    n_assets = len(prices.columns)

    ew_weights = np.ones(n_assets) / float(n_assets)
    ew_daily_rets = daily_returns.values @ ew_weights

    lookback_init = min(60, max(20, n_days // 3))
    sub_returns = daily_returns.iloc[:lookback_init]
    mu_init = sub_returns.mean().values * 252.0
    cov_init = sub_returns.cov().values * 252.0

    q_weights, _ = optimize_continuous_weights_slsqp(
        selected_indices, mu_init, cov_init
    )

    format_date = lambda d: d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]

    q_daily_rets = []
    ew_curve = [100.0]
    q_curve = [100.0]
    dates_str = [format_date(dates[0])]

    prev_weights = np.zeros(n_assets)
    cum_turnover = 0.0

    for t in range(n_days):
        day_rets = daily_returns.iloc[t].values
        gross_ret = float(np.dot(q_weights, day_rets))

        cost = 0.0
        if t % rebalance_freq_days == 0:
            turnover = float(np.sum(np.abs(q_weights - prev_weights)))
            cum_turnover += turnover
            cost = turnover * (transaction_cost_bps / 10000.0)
            prev_weights = q_weights.copy()

        net_ret = gross_ret - cost
        q_daily_rets.append(net_ret)

        q_val = q_curve[-1] * (1.0 + net_ret)
        ew_val = ew_curve[-1] * (1.0 + ew_daily_rets[t])

        q_curve.append(float(q_val))
        ew_curve.append(float(ew_val))
        dates_str.append(format_date(dates[t]))

    q_rets_arr = np.array(q_daily_rets)
    ann_ret = float(np.mean(q_rets_arr) * 252.0)
    ann_vol = float(np.std(q_rets_arr) * np.sqrt(252.0))
    sharpe = float((ann_ret - 0.04) / max(ann_vol, 1e-6))

    curve_arr = np.array(q_curve)
    peaks = np.maximum.accumulate(curve_arr)
    drawdowns = (curve_arr - peaks) / peaks
    max_drawdown = float(np.min(drawdowns) * 100.0)

    step = max(1, len(dates_str) // 40)
    chart_data = []
    for idx in range(0, len(dates_str), step):
        chart_data.append({
            "date": dates_str[idx],
            "q_frontier": round(q_curve[idx], 2),
            "benchmark_ew": round(ew_curve[idx], 2)
        })

    return {
        "final_portfolio_value": round(q_curve[-1], 2),
        "benchmark_final_value": round(ew_curve[-1], 2),
        "annualized_return_pct": round(ann_ret * 100.0, 2),
        "annualized_volatility_pct": round(ann_vol * 100.0, 2),
        "net_sharpe_ratio": round(sharpe, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "total_turnover": round(cum_turnover, 2),
        "transaction_costs_paid": round(cum_turnover * (transaction_cost_bps / 10000.0) * 100.0, 3),
        "equity_curve": chart_data
    }
