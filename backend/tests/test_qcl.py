"""
Unit Tests for Stage 2: 4-Qubit QCL Volatility Sensor
"""

import numpy as np
import pytest
from app.qcl_volatility import QCLVolatilitySensor


def test_feature_extraction():
    sensor = QCLVolatilitySensor()
    prices = 100.0 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, 60)))
    features = sensor.extract_primitive_features(prices)
    
    assert len(features) == 4
    assert np.all(features >= -1.0) and np.all(features <= 1.0)


def test_circuit_construction():
    sensor = QCLVolatilitySensor()
    x = np.array([0.2, -0.4, 0.1, -0.2])
    qc = sensor.build_circuit(x)
    
    assert qc.num_qubits == 4
    # Check gate counts: 3 layers * 4 qubits = 12 CNOTs
    op_counts = qc.count_ops()
    assert op_counts.get("cx", 0) == 12


def test_predict_volatility_and_q_bounds():
    sensor = QCLVolatilitySensor()
    x = np.array([0.5, 0.8, -0.7, 0.6])  # High volatility regime
    vol_pred, q_t = sensor.predict_volatility(x)
    
    assert 0.10 <= vol_pred <= 0.50
    assert 0.20 <= q_t <= 0.80
