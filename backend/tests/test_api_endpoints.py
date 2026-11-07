"""
Integration tests for FastAPI REST API endpoints using TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["workbench"] == "Q-FRONTIER"
    assert "SIMULATED" in data["quantum_simulation"]["mode"]


def test_datasets_endpoint(client):
    res = client.get("/api/datasets")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_validate_data_endpoint(client):
    csv_str = (
        "Date,AAPL,MSFT\n"
        "2026-01-01,150.0,300.0\n"
        "2026-01-02,152.0,302.0\n"
        "2026-01-03,151.0,301.0\n"
        "2026-01-04,153.0,305.0\n"
        "2026-01-05,154.0,304.0\n"
        "2026-01-06,155.0,306.0\n"
        "2026-01-07,156.0,307.0\n"
        "2026-01-08,157.0,309.0\n"
        "2026-01-09,158.0,310.0\n"
        "2026-01-10,159.0,312.0\n"
    )
    res = client.post("/api/validate-data", json={"csv_content": csv_str, "dataset_id": "test_upload"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid"] is True
    assert data["num_assets"] == 2


def test_create_and_fetch_run_and_export(client):
    payload = {
        "dataset_id": "synthetic_tech_4",
        "asset_count": 4,
        "k_cardinality": 2,
        "lambda_risk": 0.5,
        "covariance_method": "ledoit_wolf",
        "solvers": ["exact", "annealing", "xy_qaoa"],
        "circuit_depth": 1,
        "seeds": [42],
        "transaction_cost_bps": 5.0,
    }
    create_res = client.post("/api/runs", json=payload)
    assert create_res.status_code == 200
    run_data = create_res.json()
    run_id = run_data["run_id"]
    assert "data_fingerprint" in run_data
    assert "solver_results" in run_data
    assert len(run_data["solver_results"]) == 3

    # Fetch run
    fetch_res = client.get(f"/api/runs/{run_id}")
    assert fetch_res.status_code == 200
    assert fetch_res.json()["run_id"] == run_id

    # Fetch portfolio
    port_res = client.get(f"/api/runs/{run_id}/portfolio")
    assert port_res.status_code == 200
    assert "continuous_weights" in port_res.json()

    # Fetch export bundle
    export_res = client.get(f"/api/runs/{run_id}/export")
    assert export_res.status_code == 200
    bundle = export_res.json()
    assert bundle["run_id"] == run_id
    assert "instructions_to_reproduce" in bundle
    assert "environment" in bundle
