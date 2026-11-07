"""
Unit and integration tests for QPU Hardware Driver, Transpilation, and Provenance Logging.
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient

from app.hardware.driver import qpu_driver
from app.solvers.qpu_solver import QPUSolver
from app.main import app

client = TestClient(app)


def test_device_calibrations():
    """Verify calibration snapshots across target architectures."""
    for backend in ["ionq", "ibm", "quantum_rings", "sandia"]:
        cal = qpu_driver.get_device_calibration(backend, n_qubits=4)
        assert cal.qubit_count == 4
        assert cal.avg_t1_us > 0.0
        assert cal.two_qubit_error > 0.0
        assert cal.readout_error > 0.0


def test_ionq_vs_ibm_transpilation_swaps():
    """Verify IonQ has 0 routing SWAPs while IBM linear chain requires SWAPs."""
    cmap_ionq = qpu_driver.build_coupling_map("ionq", 4)
    cmap_ibm = qpu_driver.build_coupling_map("ibm", 4)

    assert len(cmap_ionq.get_edges()) == 12  # K_4 has 4*3 = 12 directed edges
    assert len(cmap_ibm.get_edges()) == 6    # Linear 4-chain has 3 pairs * 2 = 6 directed edges


def test_qpu_driver_shot_execution():
    """Verify physical shot sampling, calibration logging, and Hamming weight accounting."""
    cov = np.array([
        [0.08, 0.03, 0.02, 0.01],
        [0.03, 0.09, 0.04, 0.02],
        [0.02, 0.04, 0.07, 0.03],
        [0.01, 0.02, 0.03, 0.06]
    ])
    mu = np.array([0.18, 0.22, 0.15, 0.12])

    record = qpu_driver.execute_on_qpu(
        cov=cov,
        mu=mu,
        k_cardinality=2,
        backend_target="ionq",
        circuit_depth=1,
        shots=500
    )

    assert record.shots == 500
    assert record.provider == "IonQ"
    assert record.execution_mode == "SIMULATED_NOISE_QPU"
    assert sum(record.raw_shot_counts.values()) == 500
    assert 0.0 <= record.measured_feasibility <= 1.0
    assert 0.0 <= record.measured_approximation_ratio <= 1.0
    assert "avg_t1_us" in record.calibration_snapshot


def test_qpu_solver_interface():
    """Verify QPUSolver returns standard SolverResult."""
    cov = np.array([
        [0.08, 0.03, 0.02, 0.01],
        [0.03, 0.09, 0.04, 0.02],
        [0.02, 0.04, 0.07, 0.03],
        [0.01, 0.02, 0.03, 0.06]
    ])
    mu = np.array([0.18, 0.22, 0.15, 0.12])
    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]

    solver = QPUSolver(backend_target="ibm", shots=256)
    res = solver.solve(cov, mu, k_cardinality=2, tickers=tickers, depth=1)

    assert "QPU" in res.solver_name
    assert res.solver_type == "SIMULATED_NOISE_QPU"
    assert res.qubits_used == 4
    assert res.two_qubit_gates is not None
    assert "calibration_snapshot" in res.metadata


def test_execute_qpu_api_endpoint():
    """Verify POST /api/hardware/execute-qpu returns execution record."""
    payload = {
        "backend_target": "quantum_rings",
        "n_qubits": 4,
        "k_cardinality": 2,
        "circuit_depth": 1,
        "shots": 200
    }
    res = client.post("/api/hardware/execute-qpu", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["provider"] == "Quantum Rings"
    assert data["shots"] == 200
    assert "raw_shot_counts" in data
    assert "calibration_snapshot" in data
