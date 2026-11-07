"""
Cardinality-constrained Markowitz binary portfolio selection objective function.
"""

from __future__ import annotations
from typing import Tuple, List, Optional
import numpy as np


def evaluate_selection_objective(
    x: np.ndarray,
    cov: np.ndarray,
    mu: np.ndarray,
    lambda_risk: float = 0.5,
    x_prev: Optional[np.ndarray] = None,
    turnover_penalty: float = 0.0
) -> float:
    """
    Computes the scalarized binary portfolio objective:
      f(x) = lambda_risk * (x^T Sigma x) - (1 - lambda_risk) * (mu^T x) - kappa * (x_prev^T x)
    Where:
      - x in {0, 1}^N is the asset selection indicator vector.
      - Sigma is the annualized covariance matrix.
      - mu is the annualized expected return vector.
      - lambda_risk in [0, 1] is the risk-aversion constant.
      - kappa is an optional turnover continuity incentive.
    """
    x = np.asarray(x, dtype=float)
    variance = float(x @ cov @ x)
    ret = float(np.dot(mu, x))
    turnover_bonus = 0.0
    if x_prev is not None and turnover_penalty > 0.0:
        turnover_bonus = float(turnover_penalty * np.dot(x_prev, x))

    return float(lambda_risk * variance - (1.0 - lambda_risk) * ret - turnover_bonus)


def check_cardinality_feasibility(x: np.ndarray, k_cardinality: int) -> bool:
    """Checks whether binary selection vector satisfies exactly K active assets."""
    return int(np.round(np.sum(x))) == k_cardinality


def bitstring_to_vector(bitstring: str) -> np.ndarray:
    """Converts bitstring (e.g., '1010') to numpy array [1, 0, 1, 0]."""
    return np.array([int(c) for c in bitstring], dtype=float)


def vector_to_bitstring(x: np.ndarray) -> str:
    """Converts numpy array [1, 0, 1, 0] to bitstring '1010'."""
    return "".join(str(int(round(v))) for v in x)


def compute_all_bitstring_energies(
    cov: np.ndarray,
    mu: np.ndarray,
    lambda_risk: float = 0.5,
    x_prev: Optional[np.ndarray] = None,
    turnover_penalty: float = 0.0
) -> Tuple[np.ndarray, List[str]]:
    """
    Computes objective energy f(b) for all 2^N computational basis states.
    Returns: (energy_array, list_of_bitstrings)
    """
    n = len(mu)
    dim = 2 ** n
    energies = np.zeros(dim, dtype=float)
    bitstrings = []

    for i in range(dim):
        b_str = bin(i)[2:].zfill(n)
        b_vec = np.array([int(c) for c in b_str], dtype=float)
        energies[i] = evaluate_selection_objective(
            b_vec, cov, mu, lambda_risk, x_prev, turnover_penalty
        )
        bitstrings.append(b_str)

    return energies, bitstrings
