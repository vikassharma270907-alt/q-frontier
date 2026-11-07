"""
Q-FRONTIER: Auditable Hybrid Optimization Research Workbench
FastAPI Backend Server & Standardized REST API Endpoints
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schemas import RunRequest, CSVValidateRequest, OptimizationRequest, StressTestRequest
from app.hardware.models import QPUExecuteRequest
from app.hardware.driver import qpu_driver
from app.data.loader import dataset_manager
from app.data.validation import parse_and_validate_csv
from app.services.runs import run_service
from app.services.exports import export_service
from app.finance.stress_testing import run_systemic_crisis_stress_test

# Import legacy components for backward compatibility
from app.rmt_clustering import (
    DEFAULT_TICKERS,
    fetch_nasdaq_history,
    compute_expected_returns_and_covariance,
    marchenko_pastur_denoise,
    get_clusters,
)
from app.qcl_volatility import QCLVolatilitySensor
from app.caf_coordinator import CAFCoordinator
from app.slsqp_backtest import optimize_continuous_weights_slsqp, run_walk_forward_backtest
from app.hardware_benchmarks import generate_hardware_comparison, generate_sandia_volumetric_grid

app = FastAPI(
    title="Q-FRONTIER API",
    description="Auditable Hybrid-Optimization Research Workbench for Cardinality-Constrained Portfolio Selection",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

volatility_sensor = QCLVolatilitySensor()


# ---------------------------------------------------------------------------
# Core Standardized API Endpoints (as defined in Master Prompt)
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Returns platform health, simulation status, and environment capabilities."""
    qr_available = False
    try:
        import QuantumRingsLib
        qr_available = True
    except ImportError:
        pass

    aer_available = False
    try:
        from app.hardware.driver import AER_AVAILABLE
        aer_available = AER_AVAILABLE
    except Exception:
        pass

    return {
        "status": "healthy",
        "workbench": "Q-FRONTIER",
        "competition": "Intermountain Quantum Competition (IQC) 2026",
        "organizer": "Brigham Young University (BYU)",
        "sponsors": [
            "Nasdaq", "Quantum Rings", "IonQ", "Sandia National Laboratories",
            "IBM Quantum", "Classiq", "qBraid", "Aqora", "BYU Physics"
        ],
        "backends": {
            "qiskit_aer": aer_available,
            "quantum_rings_lib": qr_available,
            "ionq_transpiler": True
        },
        "version": "2.0.0",
        "disclaimer": "RESEARCH PROTOTYPE ONLY — NOT INVESTMENT ADVICE. NO QUANTUM ADVANTAGE CLAIMED.",
        "quantum_simulation": {
            "backend": "Qiskit Aer / Statevector",
            "quantum_rings_lib": qr_available,
            "mode": "SIMULATED",
        },
        "python_version": sys.version.split(" ")[0],
    }


@app.get("/api/datasets")
def list_datasets() -> List[Dict[str, Any]]:
    """Returns all available deterministic synthetic presets and uploaded datasets."""
    return dataset_manager.list_datasets()


@app.post("/api/validate-data")
def validate_data(req: CSVValidateRequest) -> Dict[str, Any]:
    """Validates raw CSV content for dates, positive prices, missingness, and asset counts."""
    is_valid, diag, clean_df = parse_and_validate_csv(req.csv_content)
    if is_valid and clean_df is not None and req.dataset_id:
        clean_id = dataset_manager.store_custom_dataset(req.dataset_id, clean_df)
        diag["dataset_id"] = clean_id
    return diag


@app.post("/api/runs")
def create_run(req: RunRequest) -> Dict[str, Any]:
    """
    Executes a multi-solver benchmark run on identical inputs and constraints.
    Compares Exact Classical Enumeration, Simulated Annealing, XY-QAOA, CCD-QAOA, and Penalty-QAOA.
    """
    try:
        run_record = run_service.execute_run(
            dataset_id=req.dataset_id,
            asset_count=req.asset_count,
            k_cardinality=req.k_cardinality,
            lambda_risk=req.lambda_risk,
            covariance_method=req.covariance_method,
            solvers=req.solvers,
            seeds=req.seeds,
            circuit_depth=req.circuit_depth,
            transaction_cost_bps=req.transaction_cost_bps,
            turnover_penalty=req.turnover_penalty,
        )
        return run_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Run execution failed: {str(e)}")


@app.get("/api/runs")
def list_runs() -> List[Dict[str, Any]]:
    """Lists history of previously executed benchmark runs."""
    return run_service.list_runs()


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> Dict[str, Any]:
    """Retrieves full metrics, solver results, and diagnostics for a specific run."""
    run = run_service.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return run


@app.get("/api/runs/{run_id}/portfolio")
def get_run_portfolio(run_id: str) -> Dict[str, Any]:
    """Retrieves the continuous allocation and financial weights for a specific run."""
    run = run_service.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return run.get("selected_portfolio", {})


@app.get("/api/runs/{run_id}/export")
def export_run_bundle(run_id: str) -> Dict[str, Any]:
    """Downloads an immutable JSON audit and reproducibility package."""
    bundle = export_service.generate_reproducibility_bundle(run_id)
    if not bundle:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return bundle


@app.post("/api/stress-test")
def execute_stress_test(req: StressTestRequest) -> Dict[str, Any]:
    """
    Executes a systemic financial crisis stress test comparing Classical Markowitz
    vs Q-FRONTIER (QCL Volatility Sensor + GNN-Sparsified CCD-QAOA).
    """
    try:
        report = run_systemic_crisis_stress_test(
            scenario=req.scenario,
            k_cardinality=req.k_cardinality,
            asset_count=req.asset_count,
            transaction_cost_bps=req.transaction_cost_bps,
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stress test simulation failed: {str(e)}")


# ---------------------------------------------------------------------------
# Backward Compatibility & Research Extension Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/market/clusters")
def get_market_clusters() -> Dict[str, Any]:
    """Ingests price history, applies Ledoit-Wolf and RMT spectral denoising, and partitions clusters."""
    try:
        prices = fetch_nasdaq_history(DEFAULT_TICKERS, lookback_days=180)
        mu, cov, tickers = compute_expected_returns_and_covariance(prices)
        denoised_cov, denoised_corr, lambda_plus = marchenko_pastur_denoise(
            cov, t_samples=len(prices), n_assets=len(tickers)
        )
        clusters = get_clusters(denoised_corr, tickers, max_cluster_size=4)

        std = np.sqrt(np.diag(cov))
        inv_std = 1.0 / np.where(std == 0, 1e-8, std)
        raw_corr = inv_std[:, None] * cov * inv_std[None, :]
        np.fill_diagonal(raw_corr, 1.0)

        return {
            "tickers": tickers,
            "expected_returns": [round(float(x), 4) for x in mu],
            "raw_correlation": [[round(float(val), 3) for val in row] for row in raw_corr],
            "denoised_correlation": [[round(float(val), 3) for val in row] for row in denoised_corr],
            "marchenko_pastur_lambda_plus": round(float(lambda_plus), 3),
            "clusters": clusters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quantum/optimize")
def run_optimization(req: OptimizationRequest) -> Dict[str, Any]:
    """Executes legacy CAF coordination pipeline with QCL sensor."""
    try:
        prices = fetch_nasdaq_history(DEFAULT_TICKERS, lookback_days=180)
        mu, cov, tickers = compute_expected_returns_and_covariance(prices)
        denoised_cov, denoised_corr, lambda_plus = marchenko_pastur_denoise(
            cov, t_samples=len(prices), n_assets=len(tickers)
        )
        clusters = get_clusters(denoised_corr, tickers, max_cluster_size=4)

        market_index_proxy = prices.mean(axis=1).values
        qcl_features = volatility_sensor.extract_primitive_features(market_index_proxy)
        pred_vol, q_dynamic = volatility_sensor.predict_volatility(qcl_features)

        q_effective = float(q_dynamic if req.use_qcl_sensor or req.q_risk is None else req.q_risk)

        coordinator = CAFCoordinator(
            denoised_cov=denoised_cov,
            expected_returns=mu,
            clusters=clusters,
            q_risk=q_effective,
            continuity_bonus=req.continuity_bonus
        )
        caf_results = coordinator.run_caf_coordination(
            k_per_cluster=2,
            max_outer_iterations=2,
            depth=req.depth
        )

        selected_indices = caf_results["selected_indices"]
        selected_tickers = [tickers[i] for i in selected_indices]

        continuous_weights, sharpe = optimize_continuous_weights_slsqp(
            selected_indices, mu, denoised_cov
        )

        backtest = run_walk_forward_backtest(
            prices=prices,
            selected_indices=selected_indices,
            transaction_cost_bps=req.transaction_cost_bps
        )

        rep_cluster_diag = caf_results["cluster_details"][0] if caf_results["cluster_details"] else {}

        return {
            "selected_tickers": selected_tickers,
            "selected_indices": selected_indices,
            "weights": [
                {"ticker": tickers[i], "weight": round(float(continuous_weights[i]), 4)}
                for i in selected_indices
            ],
            "regime_sensor": {
                "features_encoded": [round(float(x), 3) for x in qcl_features],
                "predicted_volatility": round(pred_vol * 100.0, 2),
                "dynamic_q_risk": round(q_effective, 3),
                "sensor_active": req.use_qcl_sensor
            },
            "caf_metrics": {
                "static_energy": round(float(caf_results["static_energy"]), 5),
                "caf_energy": round(float(caf_results["caf_energy"]), 5),
                "risk_reduction_pct": round(float(caf_results["risk_reduction_pct"]), 2),
                "energy_trajectory": [round(float(e), 5) for e in caf_results["energy_trajectory"]]
            },
            "quantum_solver_benchmark": {
                "depth": req.depth,
                "ccd_qaoa": rep_cluster_diag.get("ccd_qaoa", {}),
                "xy_qaoa": rep_cluster_diag.get("xy_qaoa", {}),
                "penalty_qaoa": rep_cluster_diag.get("penalty_qaoa", {}),
                "state_distribution": rep_cluster_diag.get("state_distribution", [])
            },
            "backtest": backtest
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/hardware/benchmarks")
def get_hardware_benchmarks(n_qubits: int = Query(4, ge=2, le=12)) -> Dict[str, Any]:
    """Returns IonQ all-to-all vs IBM heavy-hex SWAP routing and Sandia 2D volumetric grid."""
    try:
        hw_comp = generate_hardware_comparison(n_qubits=n_qubits)
        sandia_grid = generate_sandia_volumetric_grid()
        return {
            "hardware_comparison": hw_comp,
            "sandia_volumetric_grid": sandia_grid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/hardware/execute-qpu")
def execute_qpu_job(req: QPUExecuteRequest) -> Dict[str, Any]:
    """
    Submits circuit to target QPU architecture (IonQ, IBM, Quantum Rings, Sandia).
    Transpiles, samples measurement shots under device noise models, and logs calibration snapshot.
    """
    try:
        prices = fetch_nasdaq_history(DEFAULT_TICKERS[:req.n_qubits], lookback_days=90)
        mu, cov, _ = compute_expected_returns_and_covariance(prices)

        record = qpu_driver.execute_on_qpu(
            cov=cov,
            mu=mu,
            k_cardinality=req.k_cardinality,
            backend_target=req.backend_target,
            circuit_depth=req.circuit_depth,
            shots=req.shots,
            api_token=req.api_token
        )
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QPU execution failed: {str(e)}")


# ---------------------------------------------------------------------------
# Static SPA Frontend & Interactive Demo Video Serving
# ---------------------------------------------------------------------------

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
if docs_dir.exists():
    app.mount("/demo-assets", StaticFiles(directory=docs_dir), name="demo-assets")

    @app.get("/demo", include_in_schema=False)
    def serve_demo_video():
        demo_file = docs_dir / "video_demo_player.html"
        if demo_file.exists():
            return FileResponse(demo_file)
        raise HTTPException(status_code=404, detail="Demo video player not found")

frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend_spa(full_path: str):
        # Don't intercept API calls
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")

