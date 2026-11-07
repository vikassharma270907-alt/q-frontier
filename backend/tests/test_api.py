"""
Integration Tests for FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "Nasdaq" in data["sponsors"]
    assert data["backends"]["qiskit_aer"] is True


def test_market_clusters_endpoint():
    res = client.get("/api/market/clusters")
    assert res.status_code == 200
    data = res.json()
    assert "tickers" in data
    assert len(data["tickers"]) == 12
    assert "clusters" in data
    assert len(data["clusters"]) == 3
    assert data["marchenko_pastur_lambda_plus"] > 0


def test_quantum_optimize_endpoint():
    payload = {
        "q_risk": None,
        "continuity_bonus": 0.05,
        "depth": 1,
        "use_qcl_sensor": True,
        "transaction_cost_bps": 5.0
    }
    res = client.post("/api/quantum/optimize", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "selected_tickers" in data
    assert len(data["selected_tickers"]) == 6
    assert "regime_sensor" in data
    assert data["regime_sensor"]["sensor_active"] is True
    assert "caf_metrics" in data
    assert "quantum_solver_benchmark" in data
    assert "backtest" in data
    assert data["backtest"]["final_portfolio_value"] > 50.0


def test_hardware_benchmarks_endpoint():
    res = client.get("/api/hardware/benchmarks")
    assert res.status_code == 200
    data = res.json()
    assert "hardware_comparison" in data
    assert data["hardware_comparison"]["ionq_trapped_ion"]["routing_swaps"] == 0
    assert "sandia_volumetric_grid" in data
    assert len(data["sandia_volumetric_grid"]) == 20
