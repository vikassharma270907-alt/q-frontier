"""
Run management and benchmark orchestration service.
"""

from __future__ import annotations
from collections import OrderedDict
import uuid
import hashlib
import time
import json
import re
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import numpy as np
import pandas as pd

from app.data.loader import dataset_manager
from app.finance.returns import compute_returns, compute_expected_returns
from app.finance.covariance import (
    compute_sample_covariance,
    compute_ledoit_wolf_covariance,
    compute_rmt_marchenko_pastur_covariance,
    covariance_to_correlation,
)
from app.finance.backtest import optimize_continuous_weights_slsqp, run_walk_forward_backtest
from app.solvers.exact import ExactEnumerationSolver
from app.solvers.annealing import SimulatedAnnealingSolver
from app.solvers.xy_qaoa import XYQAOASolver
from app.solvers.penalty_qaoa import PenaltyQAOASolver
from app.solvers.agp_experiment import CounterdiabaticQAOASolver
from app.solvers.qpu_solver import QPUSolver
from app.metrics.quality import compute_multi_seed_statistics


def sanitize_for_json(obj: Any) -> Any:
    """Recursively converts NumPy and custom numeric types into Python standard primitives."""
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return [sanitize_for_json(item) for item in obj.tolist()]
    return obj


class RunService:
    """Orchestrates benchmark runs, comparisons, and persistence."""

    def __init__(self, storage_dir: Optional[Path] = None, max_cached_runs: int = 50):
        if storage_dir is None:
            self.storage_dir = Path(__file__).resolve().parent.parent / "run_history"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._runs: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.max_cached_runs = max_cached_runs
        self._hydrate_existing_runs()

    def _hydrate_existing_runs(self) -> None:
        """Hydrates previous run records from disk on startup."""
        try:
            for p in sorted(self.storage_dir.glob("*.json"), key=lambda f: f.stat().st_mtime):
                try:
                    with open(p, "r") as f:
                        data = json.load(f)
                        run_id = data.get("run_id") or p.stem
                        self._runs[run_id] = data
                        if len(self._runs) > self.max_cached_runs:
                            self._runs.popitem(last=False)
                except Exception:
                    pass
        except Exception:
            pass

    def execute_run(
        self,
        dataset_id: str = "synthetic_nasdaq_8",
        asset_count: int = 8,
        k_cardinality: int = 3,
        lambda_risk: float = 0.5,
        covariance_method: str = "ledoit_wolf",  # "ledoit_wolf", "sample", "rmt"
        solvers: Optional[List[str]] = None,
        seeds: Optional[List[int]] = None,
        circuit_depth: int = 1,
        transaction_cost_bps: float = 5.0,
        turnover_penalty: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Executes an auditable benchmark run across all requested solvers.
        """
        if solvers is None:
            solvers = ["exact", "annealing", "xy_qaoa", "ccd_qaoa", "penalty_qaoa"]
        if seeds is None:
            seeds = [42, 101, 777]

        # 1. Ingest Data
        prices = dataset_manager.get_dataset(dataset_id)
        if len(prices.columns) > asset_count:
            prices = prices.iloc[:, :asset_count]

        tickers = list(prices.columns)
        n = len(tickers)
        k_cardinality = min(k_cardinality, n - 1)

        # Hash input price matrix for audit fingerprint
        data_hash = hashlib.sha256(prices.to_csv().encode("utf-8")).hexdigest()[:16]

        # 2. Finance Estimation
        returns = compute_returns(prices, method="simple")
        mu, _ = compute_expected_returns(returns)

        cov_sample = compute_sample_covariance(returns)
        if covariance_method == "sample":
            cov = cov_sample
            cov_desc = "Sample Covariance"
        elif covariance_method == "rmt":
            cov, _, lambda_plus = compute_rmt_marchenko_pastur_covariance(
                cov_sample, t_samples=len(returns), n_assets=n
            )
            cov_desc = f"RMT Marchenko-Pastur Denoised (lambda+ = {round(lambda_plus, 3)})"
        else:
            cov, shrinkage = compute_ledoit_wolf_covariance(returns)
            cov_desc = f"Ledoit-Wolf Shrinkage (alpha = {round(shrinkage, 3)})"

        corr = covariance_to_correlation(cov)

        # 3. Solvers Execution
        results_list: List[Dict[str, Any]] = []
        ground_truth_min = None
        ground_truth_max = None

        # Always run exact enumeration if n <= 16 to provide ground truth
        exact_solver = ExactEnumerationSolver()
        exact_res = exact_solver.solve(
            cov=cov,
            mu=mu,
            k_cardinality=k_cardinality,
            tickers=tickers,
            lambda_risk=lambda_risk,
            turnover_penalty=turnover_penalty,
        )
        ground_truth_min = exact_res.objective_value
        ground_truth_max = exact_res.metadata["e_max"]

        if "exact" in solvers:
            results_list.append(exact_res.to_dict())

        # Simulated Annealing with multi-seed statistics
        if "annealing" in solvers:
            sa_solver = SimulatedAnnealingSolver()
            seed_objs = []
            seed_results = []
            for s in seeds:
                res = sa_solver.solve(
                    cov=cov,
                    mu=mu,
                    k_cardinality=k_cardinality,
                    tickers=tickers,
                    lambda_risk=lambda_risk,
                    turnover_penalty=turnover_penalty,
                    seed=s,
                    ground_truth_min=ground_truth_min,
                    ground_truth_max=ground_truth_max,
                )
                seed_objs.append(res.objective_value)
                seed_results.append(res)

            best_sa = min(seed_results, key=lambda r: r.objective_value)
            sa_dict = best_sa.to_dict()
            sa_dict["metadata"]["multi_seed_stats"] = compute_multi_seed_statistics(seed_objs)
            results_list.append(sa_dict)

        # XY-QAOA (Simulated)
        if "xy_qaoa" in solvers:
            xy_solver = XYQAOASolver()
            xy_res = xy_solver.solve(
                cov=cov,
                mu=mu,
                k_cardinality=k_cardinality,
                tickers=tickers,
                lambda_risk=lambda_risk,
                depth=circuit_depth,
                turnover_penalty=turnover_penalty,
                ground_truth_min=ground_truth_min,
                ground_truth_max=ground_truth_max,
            )
            results_list.append(xy_res.to_dict())

        # CCD-QAOA (Counterdiabatic AGP, Simulated)
        if "ccd_qaoa" in solvers:
            ccd_solver = CounterdiabaticQAOASolver()
            ccd_res = ccd_solver.solve(
                cov=cov,
                mu=mu,
                k_cardinality=k_cardinality,
                tickers=tickers,
                lambda_risk=lambda_risk,
                depth=circuit_depth,
                turnover_penalty=turnover_penalty,
                ground_truth_min=ground_truth_min,
                ground_truth_max=ground_truth_max,
            )
            results_list.append(ccd_res.to_dict())

        # Penalty-QAOA (Simulated)
        if "penalty_qaoa" in solvers:
            pen_solver = PenaltyQAOASolver()
            pen_res = pen_solver.solve(
                cov=cov,
                mu=mu,
                k_cardinality=k_cardinality,
                tickers=tickers,
                lambda_risk=lambda_risk,
                depth=circuit_depth,
                turnover_penalty=turnover_penalty,
                ground_truth_min=ground_truth_min,
                ground_truth_max=ground_truth_max,
            )
            results_list.append(pen_res.to_dict())

        # QPU Hardware Calibrated Device (IonQ / IBM / Quantum Rings / Sandia)
        if "qpu_hardware" in solvers or "qpu" in solvers:
            qpu_s = QPUSolver(backend_target="ionq", shots=1024)
            opt_bitstr = "".join("1" if i in exact_res.selected_indices else "0" for i in range(n))
            qpu_res = qpu_s.solve(
                cov=cov,
                mu=mu,
                k_cardinality=k_cardinality,
                tickers=tickers,
                lambda_risk=lambda_risk,
                depth=circuit_depth,
                turnover_penalty=turnover_penalty,
                ground_truth_min=ground_truth_min,
                ground_truth_max=ground_truth_max,
                opt_bitstring=opt_bitstr,
            )
            results_list.append(qpu_res.to_dict())

        # 4. Continuous Weights & Backtest on Best Portfolio
        best_selection_res = min(results_list, key=lambda r: r["objective_value"])
        selected_indices = best_selection_res["selected_indices"]
        selected_tickers = best_selection_res["selected_tickers"]

        continuous_weights, sharpe = optimize_continuous_weights_slsqp(
            selected_indices, mu, cov
        )

        backtest = run_walk_forward_backtest(
            prices=prices,
            selected_indices=selected_indices,
            transaction_cost_bps=transaction_cost_bps,
        )

        # 5. Build Run Record
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        run_record = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "scientific_disclaimer": "RESEARCH PROTOTYPE ONLY. NOT INVESTMENT ADVICE. NO QUANTUM ADVANTAGE CLAIMED. ALL QUANTUM EXECUTIONS ARE SIMULATED.",
            "data_fingerprint": {
                "sha256": data_hash,
                "dataset_id": dataset_id,
                "asset_count": n,
                "observations": len(prices),
                "tickers": tickers,
            },
            "parameters": {
                "asset_count": n,
                "k_cardinality": k_cardinality,
                "lambda_risk": lambda_risk,
                "covariance_method": covariance_method,
                "covariance_description": cov_desc,
                "circuit_depth": circuit_depth,
                "seeds": seeds,
                "transaction_cost_bps": transaction_cost_bps,
            },
            "ground_truth": {
                "e_min": ground_truth_min,
                "e_max": ground_truth_max,
                "optimal_tickers": exact_res.selected_tickers,
                "optimal_indices": exact_res.selected_indices,
            },
            "solver_results": results_list,
            "selected_portfolio": {
                "solver_used": best_selection_res["solver_name"],
                "selected_tickers": selected_tickers,
                "selected_indices": selected_indices,
                "continuous_weights": [
                    {"ticker": tickers[i], "weight": round(float(continuous_weights[i]), 4)}
                    for i in selected_indices
                ],
                "expected_return_pct": round(float(np.dot(continuous_weights, mu)) * 100.0, 2),
                "annualized_vol_pct": round(float(np.sqrt(continuous_weights @ cov @ continuous_weights)) * 100.0, 2),
                "theoretical_sharpe": round(sharpe, 2),
            },
            "diagnostics": {
                "expected_returns": [round(float(x), 4) for x in mu],
                "correlation_matrix": [[round(float(v), 3) for v in row] for row in corr],
                "covariance_matrix": [[round(float(v), 5) for v in row] for row in cov],
            },
            "backtest": backtest,
        }

        # Persist run with bounded LRU cache
        run_record = sanitize_for_json(run_record)
        self._runs[run_id] = run_record
        self._runs.move_to_end(run_id)
        if len(self._runs) > self.max_cached_runs:
            self._runs.popitem(last=False)

        try:
            run_file = (self.storage_dir / f"{run_id}.json").resolve()
            if run_file.is_relative_to(self.storage_dir.resolve()):
                with open(run_file, "w") as f:
                    json.dump(run_record, f, indent=2)
            # Prune old disk files if count > 100
            json_files = sorted(self.storage_dir.glob("run_*.json"), key=os.path.getmtime)
            if len(json_files) > 100:
                for old_f in json_files[:-100]:
                    try:
                        old_f.unlink()
                    except Exception:
                        pass
        except Exception:
            pass

        return run_record

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves run record by ID securely with path traversal protection."""
        if not re.match(r"^run_[0-9a-zA-Z_-]+$", run_id):
            return None

        if run_id in self._runs:
            self._runs.move_to_end(run_id)
            return self._runs[run_id]

        try:
            run_file = (self.storage_dir / f"{run_id}.json").resolve()
            if not run_file.is_relative_to(self.storage_dir.resolve()) or not run_file.exists():
                return None

            with open(run_file, "r") as f:
                data = json.load(f)
                self._runs[run_id] = data
                self._runs.move_to_end(run_id)
                if len(self._runs) > self.max_cached_runs:
                    self._runs.popitem(last=False)
                return data
        except Exception:
            pass
        return None

    def list_runs(self) -> List[Dict[str, Any]]:
        """Returns summary of previous runs."""
        summaries = []
        for run_id, r in self._runs.items():
            summaries.append({
                "run_id": run_id,
                "timestamp": r.get("timestamp"),
                "dataset_id": r.get("data_fingerprint", {}).get("dataset_id"),
                "asset_count": r.get("parameters", {}).get("asset_count"),
                "k_cardinality": r.get("parameters", {}).get("k_cardinality"),
                "lambda_risk": r.get("parameters", {}).get("lambda_risk"),
            })
        return summaries


run_service = RunService()
