# Q-FRONTIER: Implementation Plan & Architectural Blueprint

**Version:** 1.0.0  
**Date:** 8 November 2026  
**Status:** In Progress — Active Build  

---

## 1. Executive Summary

**Q-FRONTIER** is an auditable, reproducible hybrid-optimization research workbench designed for small cardinality-constrained portfolio selection problems. The objective is to rigorously and transparently compare:
1. **Exact Classical Enumeration** (ground truth for small $N \le 16$)
2. **Classical Heuristics** (Simulated Annealing with fixed compute budgets and multi-seed spread)
3. **Constraint-Preserving Quantum Simulation** (Dicke state $|D_K^N\rangle$ initialization + XY mixer QAOA preserving Hamming weight)
4. **Counterdiabatic AGP Quantum Simulation** (CCD-QAOA using 3-body adiabatic gauge potential shortcuts)
5. **Standard Penalty-QAOA** (transverse-field mixer with quadratic penalty, quantifying constraint violation/shot leakage)

### Strict Scientific Guardrails
- **No Quantum Advantage Claims:** Fair comparisons using identical objectives, risk parameters, and evaluation budgets.
- **Explicit Simulator Labeling:** Every simulation result is stamped `SIMULATED`. No `REAL_QPU` badge without explicit provider job ID, device name, and calibration metadata.
- **Statistical Rigor:** Report median and IQR across multiple random seeds, never cherry-picked single seeds.
- **Financial Integrity:** Clearly designated as an educational/research prototype, not financial or investment advice.

---

## 2. Repository Assessment

### What Already Exists
- `backend/app/ccd_qaoa_solver.py`: Prototype CCD-QAOA, XY-QAOA, and penalty-QAOA solver implementation with Dicke-statevector generation and XY mixer.
- `backend/app/qcl_volatility.py`: 4-qubit 3-layer data-reuploading QNN volatility sensor for dynamic risk-aversion scaling ($\lambda_t$).
- `backend/app/rmt_clustering.py`: Nasdaq synthetic data generator, Ledoit-Wolf shrinkage, Marchenko-Pastur RMT spectral filtering, and correlation-based asset clustering.
- `backend/tests/`: 10 passing unit tests verifying Dicke properties, XY mixer commutation, RMT filtering, and QCL circuit properties.

### What Is Missing (To Build in This Plan)
1. **Modular Architecture:**
   - `backend/app/data/`: `loader.py`, `validation.py`, `synthetic.py`
   - `backend/app/finance/`: `returns.py`, `covariance.py`, `objective.py`, `backtest.py`
   - `backend/app/solvers/`: `exact.py`, `annealing.py`, `xy_qaoa.py`, `penalty_qaoa.py`, `agp_experiment.py`, `base.py`
   - `backend/app/metrics/`: `quality.py`, `resources.py`
   - `backend/app/services/`: `runs.py`, `exports.py`
   - `backend/app/schemas.py`: Pydantic input/output schemas
   - `backend/app/main.py`: Full FastAPI application with all 7 API endpoints
2. **Interactive Frontend:**
   - Full React + Vite + TypeScript + Tailwind CSS application with Lucide icons and Recharts
   - Dataset selection & custom CSV upload with validation
   - Parameter controls ($N$, $K$, $\lambda$, seeds, circuit depth, covariance method)
   - Real-time solver execution and comparison dashboard
   - Probability distribution visualization across basis states
   - Correlation/covariance matrix heatmaps
   - Reproducibility bundle export (`.json`)
3. **Documentation & Packaging:**
   - `docs/methodology.md`: Mathematical definitions, Hamiltonians, and metrics
   - `docs/reproducibility.md`: Seed guidelines, data hashes, and verification protocol
   - `README.md`: Complete setup, API reference, and usage guide
   - `docker-compose.yml`: Multi-stage Docker configuration

---

## 3. Phased Implementation Roadmap

### Phase 0: Deterministic Core & Finance Pipeline
- [x] Extract and verify synthetic data generator with deterministic seeding.
- [x] Ingest & validate CSV data (date checking, numeric validation, missingness, duplicate handling).
- [x] Implement returns calculation (simple & log returns, annualized mean returns).
- [x] Implement covariance estimators (Sample covariance, Ledoit-Wolf shrinkage, RMT Marchenko-Pastur filtering).
- [x] Implement binary Markowitz objective:
  $$\min_{x \in \{0, 1\}^N} \lambda x^T \Sigma x - (1 - \lambda) \mu^T x \quad \text{s.t.} \quad \sum_{i=1}^N x_i = K$$
- [x] Implement exact brute-force combinatorial solver as ground truth.
- [x] Implement simulated annealing solver with multi-seed execution and Hamming weight maintenance.

### Phase 1: Quantum Simulation Baselines
- [x] Dicke-state initializer $|D_K^N\rangle$ over exact $\binom{N}{K}$ subspace.
- [x] XY mixer operator $H_M^{XY} = \sum_{i < j} (X_i X_j + Y_i Y_j)$ conserving Hamming weight.
- [x] Standard XY-QAOA parameterized circuit simulation.
- [x] Penalty-QAOA baseline with transverse field mixer $H_M^X = \sum_i X_i$ and penalty $\rho (\sum x_i - K)^2$.
- [x] AGP Counterdiabatic extension (CCD-QAOA) utilizing 3-body commutator $i [H_C, H_M^{XY}]$.
- [x] Multi-seed statistical evaluator computing median, IQR, min, max for approximation ratio and optimal probability.

### Phase 2: FastAPI Backend Services & Endpoints
- [x] Pydantic schemas for requests, run configurations, solver results, and export bundles.
- [x] Local storage/persistence service for run history (in-memory + SQLite/JSON).
- [x] Implement endpoints:
  - `GET /api/health`
  - `GET /api/datasets`
  - `POST /api/validate-data`
  - `POST /api/runs`
  - `GET /api/runs/{run_id}`
  - `GET /api/runs/{run_id}/portfolio`
  - `GET /api/runs/{run_id}/export`
- [x] CORS middleware and static file mounting.

### Phase 3: Research Dashboard Frontend
- [x] Initialize Vite + React + TypeScript + Tailwind CSS application in `frontend/`.
- [x] Build UI components:
  - Navigation bar with scientific integrity badge and project metadata.
  - Data manager panel with sample datasets and CSV drag-and-drop validation.
  - Configuration controls: $N, K, \lambda$, covariance selector, solver toggles, seed budget.
  - Metrics comparison table and cards.
  - Visual charts: Objective values, approximation ratios, feasibility comparison, statevector probability distribution, correlation heatmap.
  - One-click "Export Reproducibility Bundle" downloader.

### Phase 4: Full System Verification & Documentation
- [x] Comprehensive pytest test suite covering finance math, solvers, API endpoints, and serialization.
- [x] Create `docs/methodology.md` and `docs/reproducibility.md`.
- [x] Create root `README.md` and `docker-compose.yml`.
- [x] Run full end-to-end integration test validating frontend build and backend execution.
