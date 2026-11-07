"""
Reproducibility bundle export service for audit compliance and peer review.
"""

from __future__ import annotations
import platform
import sys
from typing import Dict, Any, Optional
import numpy as np
import qiskit
import sklearn

from app.services.runs import run_service


class ExportService:
    """Generates immutable JSON audit bundles and reproducibility logs."""

    @staticmethod
    def generate_reproducibility_bundle(run_id: str) -> Optional[Dict[str, Any]]:
        run = run_service.get_run(run_id)
        if not run:
            return None

        # System environment snapshot
        env_snapshot = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "os_name": platform.system(),
            "numpy_version": np.__version__,
            "qiskit_version": qiskit.__version__,
            "scikit_learn_version": sklearn.__version__,
        }

        bundle = {
            "bundle_title": "Q-FRONTIER Auditable Reproducibility Package",
            "run_id": run["run_id"],
            "generated_at": run["timestamp"],
            "disclaimer": run["scientific_disclaimer"],
            "environment": env_snapshot,
            "input_data_fingerprint": run["data_fingerprint"],
            "hyperparameters": run["parameters"],
            "ground_truth_reference": run["ground_truth"],
            "solvers_benchmark": run["solver_results"],
            "selected_portfolio": run["selected_portfolio"],
            "backtest_summary": {
                "final_portfolio_value": run["backtest"].get("final_portfolio_value"),
                "benchmark_final_value": run["backtest"].get("benchmark_final_value"),
                "net_sharpe_ratio": run["backtest"].get("net_sharpe_ratio"),
                "annualized_return_pct": run["backtest"].get("annualized_return_pct"),
                "annualized_volatility_pct": run["backtest"].get("annualized_volatility_pct"),
                "max_drawdown_pct": run["backtest"].get("max_drawdown_pct"),
                "transaction_costs_paid": run["backtest"].get("transaction_costs_paid"),
            },
            "instructions_to_reproduce": [
                f"1. Select dataset: '{run['data_fingerprint']['dataset_id']}' with SHA-256 fingerprint '{run['data_fingerprint']['sha256']}'.",
                f"2. Set asset universe to {run['parameters']['asset_count']} assets: {run['data_fingerprint']['tickers']}.",
                f"3. Set cardinality constraint K={run['parameters']['k_cardinality']}.",
                f"4. Set risk aversion lambda={run['parameters']['lambda_risk']}.",
                f"5. Apply covariance method: {run['parameters']['covariance_method']}.",
                f"6. Execute exact enumeration and quantum simulation (depth p={run['parameters']['circuit_depth']}).",
                "7. Compare objective values and approximation ratios against ground truth.",
            ],
        }

        return bundle


export_service = ExportService()
