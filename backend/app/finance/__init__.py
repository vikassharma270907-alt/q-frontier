"""Finance module for Q-FRONTIER."""

from app.finance.returns import compute_returns, compute_expected_returns
from app.finance.covariance import (
    compute_sample_covariance,
    compute_ledoit_wolf_covariance,
    compute_rmt_marchenko_pastur_covariance,
    covariance_to_correlation,
)
from app.finance.objective import (
    evaluate_selection_objective,
    check_cardinality_feasibility,
    bitstring_to_vector,
    vector_to_bitstring,
    compute_all_bitstring_energies,
)
from app.finance.backtest import (
    optimize_continuous_weights_slsqp,
    run_walk_forward_backtest,
)

__all__ = [
    "compute_returns",
    "compute_expected_returns",
    "compute_sample_covariance",
    "compute_ledoit_wolf_covariance",
    "compute_rmt_marchenko_pastur_covariance",
    "covariance_to_correlation",
    "evaluate_selection_objective",
    "check_cardinality_feasibility",
    "bitstring_to_vector",
    "vector_to_bitstring",
    "compute_all_bitstring_energies",
    "optimize_continuous_weights_slsqp",
    "run_walk_forward_backtest",
]
