# Q-FRONTIER

> **Auditable Hybrid Optimization Research Workbench for Cardinality-Constrained Portfolio Selection**  
> Developed for the **Intermountain Quantum Competition (IQC) 2026** (Brigham Young University).

[![Tests](https://img.shields.io/badge/pytest-32%20passed-emerald)](file:///backend/tests)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-Aer%20Simulated-cyan)](https://qiskit.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-slate)](LICENSE)

---

## ⚠️ Scientific & Financial Guardrail Disclosure

> [!IMPORTANT]
> **Research Prototype Only — Not Financial Advice — No Quantum Advantage Claimed**  
> - **Transparent Simulation Mode:** All quantum circuits are simulated via exact statevector evolution (Qiskit Aer / Statevector). No physical QPU quantum advantage or commercial trading capability is claimed.
> - **Fair Benchmark Parity:** Quantum solvers are evaluated against exact combinatorial ground truth ($N \le 16$) and Simulated Annealing heuristics using **identical input returns, covariance matrices, and risk constraints**.
> - **Reproducible Integrity:** All numerical claims are backed by deterministic random seeds and SHA-256 data fingerprinting.

---

## 1. System Architecture & Solvers

Q-FRONTIER investigates whether constraint-preserving quantum mixers can optimize small cardinality-constrained portfolios ($K$ out of $N$ assets) without leaking probability into infeasible bitstrings:

$$\min_{x \in \{0, 1\}^N} \quad f(x) = \lambda \cdot x^T \Sigma x - (1 - \lambda) \cdot \mu^T x \quad \text{subject to} \quad \sum_{i=1}^N x_i = K$$

```
+-------------------------------------------------------------------------------------------------+
|                                    Q-FRONTIER WORKBENCH                                         |
+-------------------------------------------------------------------------------------------------+
                                                 |
             +-----------------------------------+-----------------------------------+
             |                                                                       |
     [Data Ingestion]                                                        [Covariance]
     - Synthetic Nasdaq-12/8/4                                               - Sample Covariance
     - Custom CSV Price Ingestion                                            - Ledoit-Wolf Shrinkage
     - SHA-256 Data Fingerprinting                                           - RMT Marchenko-Pastur
             |                                                                       |
             +-----------------------------------+-----------------------------------+
                                                 |
                   +-----------------------------+-----------------------------+
                   |                             |                             |
          [Classical Exact]             [Classical Heuristic]         [Quantum Simulation]
          - Brute-Force Combinatorial   - Simulated Annealing         - Dicke State |D_K^N> Initializer
          - Exact Optimum (Ground Truth)- Multi-Seed Median/IQR       - Complete-Graph XY Mixer
          - Worst Feasible (AR Anchor)  - Strict Hamming Swaps        - Counterdiabatic AGP (CCD-QAOA)
                   |                             |                    - Penalty-QAOA (Shot Leakage)
                   +-----------------------------+-----------------------------+
                                                 |
                                     [Continuous Allocation]
                                     - SLSQP Sharpe Maximization
                                     - Net 5 bps Walk-Forward Backtest
                                                 |
                                     [Reproducibility Bundle]
                                     - Cryptographic JSON Audit Package
```

### Supported Benchmark Solvers

1. **Exact Classical Enumeration (`CLASSICAL_EXACT`):**
   - Evaluates all $\binom{N}{K}$ candidate binary vectors.
   - Provides absolute mathematical ground truth ($E_{\min}$ and $E_{\max}$) for rigorous calculation of Approximation Ratios.
2. **Simulated Annealing Heuristic (`CLASSICAL_HEURISTIC`):**
   - Explores the feasible subspace using pairwise index swaps ($x_i \leftrightarrow x_j$), preserving Hamming weight $K$ at every step ($100\%$ feasibility).
   - Reports multi-seed median and interquartile range (IQR).
3. **Constraint-Preserving XY-QAOA (`SIMULATED_QUANTUM`):**
   - Initializes register in uniform Dicke state $|D_K^N\rangle$.
   - Drives evolution with complete-graph XY mixer $H_M^{XY} = \sum_{i<j} (X_i X_j + Y_i Y_j)$ which commutes with the Hamming operator ($[H_M^{XY}, \sum Z_i] = 0$).
4. **Counterdiabatic AGP Extension / CCD-QAOA (`SIMULATED_QUANTUM`):**
   - Introduces normalized 3-body commutator drive $H_{CD} = i [H_C, H_M^{XY}] / \|[H_C, H_M^{XY}]\|_2$.
   - Suppresses diabatic transitions at shallow depth ($p=1, 2$), enhancing ground-state probability mass.
5. **Penalty-QAOA Baseline (`SIMULATED_QUANTUM`):**
   - Unconstrained transverse field mixer $H_M^X = \sum X_i$ with penalty $\rho (\sum x_i - K)^2$.
   - Quantifies shot leakage (typically $>5\%-20\%$ non-feasible shots), demonstrating why constraint-preserving XY mixers are mathematically superior for cardinality constraints.

---

## 2. Quickstart Guide

### 1. Unified Local Launch (Single Command)
Runs the FastAPI REST API and serves the production React dashboard on a single port:

```bash
# Launch unified server (FastAPI + React Dashboard)
python scripts/run_app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### 2. Run Comprehensive Test Suite
```bash
pytest
```
Executes all 32 unit and integration tests across data validation, covariance estimators, objective correctness, Dicke state properties, XY mixer commutation, and REST API endpoints.

### 3. Docker Compose Deployment
```bash
docker compose up --build
```
Builds the multi-stage image (Node.js Vite frontend + Python 3.11 backend) and exposes the dashboard at `http://localhost:8000`.

---

## 3. Standardized REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Platform status, backend mode (`SIMULATED`), and sponsor details |
| `GET` | `/api/datasets` | List deterministic synthetic universes and uploaded datasets |
| `POST` | `/api/validate-data` | Validate raw CSV price data (dates, positive prices, missingness) |
| `POST` | `/api/runs` | Execute benchmark suite across exact, heuristic, and quantum solvers |
| `GET` | `/api/runs` | List run history summaries |
| `GET` | `/api/runs/{run_id}` | Retrieve complete results, solver metrics, and diagnostics |
| `GET` | `/api/runs/{run_id}/portfolio` | Retrieve SLSQP continuous weights for the selected portfolio |
| `GET` | `/api/runs/{run_id}/export` | Download cryptographic JSON reproducibility bundle |

---

## 4. Repository Structure

```text
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI server and REST endpoints
│   │   ├── schemas.py                  # Pydantic request/response schemas
│   │   ├── data/
│   │   │   ├── synthetic.py            # Deterministic seeded synthetic generators
│   │   │   ├── loader.py               # Dataset manager & cache
│   │   │   └── validation.py           # CSV data integrity validator
│   │   ├── finance/
│   │   │   ├── returns.py              # Log/simple returns & expected returns
│   │   │   ├── covariance.py           # Sample, Ledoit-Wolf & RMT covariance
│   │   │   ├── objective.py            # Markowitz 0-1 quadratic objective & energies
│   │   │   └── backtest.py             # SLSQP allocation & net 5 bps backtest
│   │   ├── solvers/
│   │   │   ├── base.py                 # SolverResult contract
│   │   │   ├── exact.py                # Exact combinatorial enumeration
│   │   │   ├── annealing.py            # Simulated Annealing with multi-seed stats
│   │   │   ├── xy_qaoa.py              # Dicke state + XY mixer simulator
│   │   │   ├── penalty_qaoa.py         # Transverse mixer + quadratic penalty
│   │   │   └── agp_experiment.py       # Counterdiabatic AGP CCD-QAOA
│   │   ├── metrics/
│   │   │   ├── quality.py              # Approximation ratios & seed statistics
│   │   │   └── resources.py            # Circuit depth & 2-qubit gate overhead
│   │   ├── services/
│   │   │   ├── runs.py                 # Benchmark orchestration & persistence
│   │   │   └── exports.py              # Reproducibility JSON package builder
│   │   ├── ccd_qaoa_solver.py          # Legacy modular solver shim
│   │   ├── qcl_volatility.py           # 4-qubit QCL volatility sensor
│   │   ├── rmt_clustering.py           # RMT Marchenko-Pastur clustering
│   │   ├── caf_coordinator.py          # Context-Aware Folding coordinator
│   │   └── hardware_benchmarks.py      # IonQ vs IBM SWAP routing & Sandia grid
│   └── tests/
│       ├── test_data_validation.py     # CSV & synthetic dataset tests
│       ├── test_finance_core.py        # Returns, covariance & objective tests
│       ├── test_solvers_benchmarks.py  # Exact vs heuristic vs quantum comparisons
│       ├── test_api_endpoints.py       # REST API integration tests
│       └── ...                         # 32 passing test suites
├── frontend/
│   ├── src/
│   │   ├── App.jsx                     # Dashboard root with tab navigation
│   │   ├── components/
│   │   │   ├── AuditWorkbenchView.jsx  # Main auditable benchmark view
│   │   │   ├── Header.jsx              # Status header with scientific disclaimer
│   │   │   ├── QaoaBenchmarkView.jsx   # CCD-QAOA parameter tuning
│   │   │   ├── RmtClusterView.jsx      # Spectral denoising & correlation heatmap
│   │   │   ├── EquityCurveView.jsx     # Net walk-forward backtest curves
│   │   │   └── VolumetricView.jsx      # Sandia volumetric capability grid
│   │   └── index.css                   # Tailwind CSS styling
│   └── dist/                           # Pre-compiled static assets
├── docs/
│   ├── IMPLEMENTATION_PLAN.md          # Phased engineering roadmap
│   ├── methodology.md                  # Complete mathematical specifications
│   └── reproducibility.md              # Seeding, hashing & replication guide
├── scripts/
│   └── run_app.py                      # Local development launcher
├── reproducibility_bundle_sample.json  # Sample output audit package
├── docker-compose.yml                  # Docker Compose configuration
├── Dockerfile                          # Multi-stage production container
└── pytest.ini                          # Pytest configuration
```

---

## 5. Known Limitations & Research Roadmap

1. **Statevector Simulation Bounds:** Current statevector simulation is practical up to $N = 12$ assets on standard workstations due to the $2^N$ exponential statevector memory footprint. Instances with $N > 12$ require tensor network contraction or hardware execution.
2. **Hardware Execution Protocol:** Submitting circuits to real QPUs (IonQ, IBM, Rigetti) requires recording provider job IDs, backend names, calibration snapshots, shots, and transpiled gate decompositions into the audit bundle.
3. **Turnover Continuity:** Dynamic rebalancing across consecutive market periods can be regularized using the $\kappa \cdot x_{\text{prev}}^T x$ turnover penalty term.

---

## 6. Academic References

- **Falla & Safro (2026):** *Constrained Counterdiabatic Quantum Optimization*, arXiv:2605.06858v1.
- **Cadavid et al. (2026):** *Combinatorial Optimization via Subspace Mixers*, arXiv:2602.23976v1.
- **Proctor, Rudinger et al. (2022):** *Measuring the Capabilities of Quantum Processors without Circuit Compilation*, Nature Physics 18, 75–79.
- **Yang, Dou & Guo (2026):** *Context-Aware Folding for Multi-Cluster Quantum Optimization*, arXiv:2609.15708.
- **Ledoit & Wolf (2004):** *A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices*, Journal of Multivariate Analysis.
