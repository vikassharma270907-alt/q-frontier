"""
Solution quality metrics and multi-seed statistical aggregator.
"""

from __future__ import annotations
from typing import Dict, Any, List
import numpy as np


def calculate_approximation_ratio(
    objective_value: float,
    ground_truth_min: float,
    ground_truth_max: float
) -> float:
    """
    Computes normalized approximation ratio:
    AR = (E_max - E) / (E_max - E_min).
    Values lie in [0, 1] where 1.0 represents the exact optimum.
    """
    e_range = max(ground_truth_max - ground_truth_min, 1e-8)
    return float(np.clip((ground_truth_max - objective_value) / e_range, 0.0, 1.0))


def compute_multi_seed_statistics(values: List[float]) -> Dict[str, float]:
    """
    Calculates robust statistical metrics across multiple random seed runs:
    median, 25th percentile (Q1), 75th percentile (Q3), interquartile range (IQR),
    minimum, maximum, and standard deviation.
    """
    if not values:
        return {
            "median": 0.0,
            "q1": 0.0,
            "q3": 0.0,
            "iqr": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std": 0.0,
            "count": 0,
        }

    arr = np.asarray(values, dtype=float)
    q1 = float(np.percentile(arr, 25))
    q3 = float(np.percentile(arr, 75))
    return {
        "median": round(float(np.median(arr)), 4),
        "q1": round(q1, 4),
        "q3": round(q3, 4),
        "iqr": round(float(q3 - q1), 4),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "std": round(float(np.std(arr)), 4),
        "count": len(values),
    }
