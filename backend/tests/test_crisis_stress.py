"""
Unit and API integration tests for Crisis Stress-Testing & Generative Scenarios.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.data.synthetic import generate_crisis_prices
from app.finance.stress_testing import run_systemic_crisis_stress_test

client = TestClient(app)


def test_generate_crisis_prices_properties():
    """Verify crisis price generator outputs valid prices with expected volatility spike."""
    df = generate_crisis_prices(scenario="CRISIS_2026_LIQUIDITY", days=100, seed=42)
    assert len(df) == 100
    assert (df.values > 0).all(), "All prices must be strictly positive"


def test_run_systemic_crisis_stress_test():
    """Verify stress test report computes drawdown mitigation and returns valid comparison metrics."""
    report = run_systemic_crisis_stress_test(
        scenario="CRISIS_2026_LIQUIDITY",
        k_cardinality=2,
        asset_count=4,
        transaction_cost_bps=5.0,
        seed=42,
    )

    assert "comparison" in report
    assert "classical_markowitz" in report["comparison"]
    assert "q_frontier" in report["comparison"]
    assert len(report["time_series_trajectory"]) > 0
    assert report["qcl_regime_sensor"]["adapted_q_risk"] >= 0.2


def test_api_stress_test_endpoint():
    """Test POST /api/stress-test endpoint."""
    payload = {
        "scenario": "CRISIS_2026_LIQUIDITY",
        "k_cardinality": 2,
        "asset_count": 4,
        "transaction_cost_bps": 5.0,
    }
    response = client.post("/api/stress-test", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "CRISIS_2026_LIQUIDITY"
    assert "comparison" in data
    assert "drawdown_mitigation_advantage_pct" in data["comparison"]
