# Q-FRONTIER — Research Audit, Product Decision & Engineering Blueprint
**Prepared: 8 November 2026**  
**Primary source reviewed:** *IQC Hackathon Research And Blueprint.docx* and its PDF counterpart, supplied by the user.

## 1. Executive verdict
**Retain the portfolio-optimization problem, but narrow and rename the first release as a reproducible hybrid-optimization research workbench.** The supplied proposal has a coherent problem area—cardinality-constrained portfolio selection—and a useful judge-facing angle: compare a constraint-preserving quantum-inspired/quantum-circuit workflow against transparent classical baselines on the same data and constraints. Its present scope is too broad for a credible MVP. RMT denoising, multi-cluster coordination, a learned volatility controller, counterdiabatic QAOA, QPU benchmarking, and a polished full-stack dashboard are six substantial research/engineering projects, not one hackathon MVP.

Do not present the supplied numerical results as independently validated. The source documents assert exact solver probabilities, CAF risk reductions, QCL R², IC/hit-rate results, and backtest uplift, but the files do not provide the executable code, raw datasets, parameter files, seeds, complete objective definitions, optimizer settings, train/test split manifests, or reproducibility logs needed to reproduce those values. The word “verified” in the source is therefore a claim made by the document, not a verification finding in this audit.

**Recommended one-sentence story:** “Q-FRONTIER is an auditable workbench that tests whether constraint-preserving quantum optimization methods can produce competitive feasible portfolios on small, reproducible financial instances—and shows exactly where classical methods remain stronger.”

## 2. Source-derived proposal: what the supplied files describe
The DOCX and PDF describe substantially the same Q-FRONTIER concept:
- A Nasdaq-oriented equity universe with return/covariance estimation and Ledoit–Wolf shrinkage.
- Random Matrix Theory / Marchenko–Pastur spectral filtering and asset clustering.
- Context-Aware Folding (CAF) to pass cross-cluster context.
- A data-reuploading quantum circuit learning (QCL/QNN) volatility estimator to influence risk aversion.
- Cardinality-constrained subproblems initialized in Dicke states and evolved with XY mixers; a counterdiabatic / adiabatic-gauge-potential (AGP) extension is proposed.
- A walk-forward portfolio evaluation with transaction costs and comparisons to simulated annealing / hierarchical risk parity.
- A React dashboard and Python API, with QuantumRingsLib, Qiskit Aer, and potential sponsor hardware integrations.

The source also recommends 4–16-qubit clusters, with some later caution suggesting 4–5 qubits. The first release should use 4–8 assets per exact-solver instance, not claim a scalable 40-asset quantum solve.

## 3. Forensic audit: unsupported or risky claims
| Source claim | Audit status | What is required before it can be used |
|---|---|---|
| IQC ran Nov 6–7, 2026; final presentations Nov 7 at 15:00 MST | Source-reported; date is now past (current date Nov 8, 2026) | Official event page / archived rules and organizer confirmation. Treat as retrospective unless official evidence says otherwise. |
| 12 sponsors, 3 tracks, 7–32 participants, $850 direct / $2,000 total awards | Unverified from supplied files | Official event pages and prize rules; participant counts from dated snapshots. The $250 second prize is explicitly described as deduced, not directly confirmed. |
| “4-qubit CCD-QAOA p=1 AR 0.9568 / P(opt)=95.50%; p=2 AR 0.9977 / P(opt)=99.72%” | Not reproducible from supplied artifacts | Circuit definition, cost Hamiltonian, normalization for AR, AGP truncation, parameter optimization, seeds, shots/statevector, exact optimum, and code. |
| XY-QAOA and penalty-QAOA comparison numbers | Not reproducible from supplied artifacts | Same objective/normalization, equal optimizer budgets, multiple seeds, exact feasible-state accounting, and raw results. |
| CAF reduces risk 10.68–13.84% | Unverified | Full paper and exact algorithm; define risk measure, benchmark, sample period, universe, and statistical uncertainty. |
| QCL volatility model achieves R²=0.97783 | Unverified / likely high overfit risk | Paper and code, target definition, chronological split, leakage controls, benchmark models, multiple assets/regimes, confidence intervals. |
| Hybrid QKRR IC 0.0606 / 78.3% hit rate | Unverified | Full paper, sample selection, factor/label construction, multiple-testing correction, and out-of-sample protocol. |
| 2025 backtest portfolio value ~25% higher than simulated annealing | Unverified and financially ambiguous | Full return series, baseline parity, turnover/fees/slippage, rebalance schedule, survivorship/look-ahead controls, risk-adjusted metrics. |
| Q-VIRA competitor teardown and claimed AUC edge | Unverified third-party claims | Inspect the live Devpost entry/repository and reproduce independently; avoid competitor disparagement or repeating performance claims as facts. |

### Important internal consistency issues
1. The document uses both “4–16 qubits” and a later practical recommendation of 4–5 qubits; choose a measured cap based on backend/runtime and circuit depth.
2. It describes a 4-qubit QCL estimator with 36 parameters and 12 CX gates, but does not supply its exact circuit, data scaling, training protocol, or leakage-safe split.
3. It combines portfolio selection and continuous weight refinement. These must be separated in the objective and evaluation: the discrete stage chooses assets; a clearly specified continuous optimizer assigns weights.
4. It mixes “optimality,” approximation ratio, probability of sampling the optimum, and portfolio risk reduction. These are different metrics and must never be interchanged.
5. It proposes “real QPU” and sponsor hardware narratives while also relying on statevector/simulator results. Simulator evidence is not hardware evidence.
6. A historical backtest is not proof of future returns or investment performance.

## 4. Literature and event verification protocol
The bibliography in the supplied documents lists several 2025–2026 arXiv identifiers, including 2605.06858, 2602.14827, 2604.19832, 2602.23976, 2609.15708, 2610.00736, 2504.06253, 2510.11153, 2509.01496, 2509.18530, 2305.00905, and 2607.20168. The source file alone does not establish that each title, author list, version, result, or interpretation is correct. Treat this bibliography as a **verification queue**, not as a validated literature review. For each identifier, record: canonical arXiv landing page, title/authors/version/date, abstract, relevant equation/table/page, whether the cited numerical result appears in the paper, whether code/data are public, and whether the source is peer reviewed or a preprint. If a citation cannot be found or does not support the associated claim, remove it from the pitch.

Useful primary portals to check:
- IQC event / rules: https://iqc.devpost.com/ and https://iqc.devpost.com/rules
- Organizer: https://intermountainquantum.org/
- Aqora challenge index: https://aqora.io/challenges
- arXiv identifier lookup: https://arxiv.org/
- Quantum Rings docs: https://www.quantumrings.com/doc/
- IBM Quantum / Qiskit docs: https://quantum.ibm.com/ and https://qiskit.org/
- IonQ docs: https://docs.ionq.com/

**Date handling:** As of 8 Nov 2026, the stated Nov 6–7 event window has elapsed. Do not use the source's “4.5 hours remaining” or “hard deadline” instructions. If this is intended for a different event, update the event identity, dates, rules, and judging criteria from its official materials.

## 5. Recommended MVP (credible and demoable)
### MVP objective
For a small universe of 4–8 assets and a fixed cardinality K, compare:
1. Exact classical enumeration (ground truth for small N).
2. A classical heuristic (simulated annealing or greedy/local search).
3. Standard penalty-QAOA (optional baseline).
4. Constraint-preserving XY-QAOA using a Dicke-state feasible initialization.

Keep the counterdiabatic/AGP extension as an experimental branch only after the XY baseline is correct. Do not include a learned QCL risk controller or CAF in MVP v1; use a transparent, user-selected risk-aversion parameter. Add RMT denoising only as an optional preprocessing ablation.

### MVP user journey
1. Select a small preloaded dataset or upload a clean CSV of adjusted close prices.
2. Inspect returns, missingness, and covariance diagnostics.
3. Set N, K, risk-aversion λ, rebalance date, and transaction-cost assumption.
4. Run exact enumeration and classical baseline.
5. Run simulator-backed XY-QAOA (and optional penalty-QAOA).
6. Compare objective values, feasibility, optimum-sampling probability, runtime, circuit width/depth, and seed variability.
7. Export a reproducibility bundle: config, data fingerprint, seed, environment, solver settings, and result JSON/CSV.

### Objective
For binary selection vector x∈{0,1}ⁿ, require 1ᵀx=K. A simple, explicit objective is:
**minimize**  λ xᵀΣx − (1−λ) μᵀx  
subject to 1ᵀx=K, xᵢ∈{0,1}.
Here μ is the estimated expected-return vector, Σ is the covariance matrix, and λ∈[0,1] is a user-controlled risk/return trade-off. State units and annualization conventions. This is a selection objective, not a fully invested weighted portfolio. For a second-stage continuous allocation, solve a separate constrained problem over selected assets and report it separately.

### Algorithms
- Build returns from adjusted closes; remove/flag missing and stale observations.
- Use a chronological training window only; estimate μ and Σ on training data.
- Compare sample covariance against Ledoit–Wolf shrinkage.
- Optional RMT filtering: estimate the noise bulk threshold under an explicitly stated assumptions model; report sensitivity to window length and asset count.
- Enumerate all feasible combinations for N≤16 to obtain exact optimum and validate objective calculations.
- Classical heuristic: simulated annealing with fixed compute budget and multiple seeds; report best/median/worst.
- Quantum simulator: Dicke-state initialization and XY mixer preserving Hamming weight; use a clearly specified gate decomposition and optimizer budget.
- Optional AGP: implement only after a unit-tested XY implementation; compare equal-depth and equal-two-qubit-gate-budget variants.

## 6. Evaluation plan and acceptance criteria
### Functional acceptance
- All portfolios satisfy exactly K selected assets.
- The objective implementation matches brute-force enumeration on at least 20 random toy instances.
- Identical μ, Σ, constraints, and cost conventions are used across solvers.
- Runs are reproducible from a saved config and seed.
- UI labels simulator results as “simulated”; no QPU badge unless a real job ID and backend metadata are recorded.

### Scientific acceptance
- At least 30 random small instances across multiple N/K settings.
- Report median, interquartile range, and best/worst—not a single favorable seed.
- Compare solution quality to exact optimum, runtime, feasibility, number of circuit evaluations, and circuit resources.
- Ablations: sample vs shrinkage covariance; XY vs penalty constraint; with/without AGP; optimizer budget; noise-free vs noisy simulator.
- For financial backtests, use rolling/expanding chronological splits, no look-ahead, no survivorship bias where avoidable, realistic turnover costs, and benchmark parity.
- Report Sharpe, volatility, max drawdown, turnover, cumulative return, and confidence intervals; never report only terminal portfolio value.

### Do not claim
- Quantum advantage, quantum supremacy, production-ready investment advice, guaranteed returns, or hardware execution without evidence.
- A simulator’s exact-statevector optimum probability as a real device success probability.
- A backtest uplift as predictive evidence without robust out-of-sample validation.

## 7. Implementation architecture
**Frontend:** React + Vite + TypeScript + Tailwind + Recharts.  
**Backend:** Python 3.11+, FastAPI, Pydantic, NumPy, SciPy, pandas, scikit-learn, Qiskit + Aer (or a single simulator stack selected after compatibility checks).  
**Storage:** local SQLite or filesystem for run metadata; immutable CSV/JSON exports.  
**Deployment:** frontend on Vercel/Netlify; backend on Render/Fly.io or a single Docker deployment.  
**Data:** deterministic synthetic dataset bundled for offline demo; optional yfinance adapter with cache and clear data-source/date labels. Avoid making a live internet data source a hard demo dependency.

### Suggested repository layout
```text
q-frontier/
  frontend/
    src/{components,pages,api,charts,types}/
  backend/
    app/
      main.py
      schemas.py
      data/{loader.py,validation.py,synthetic.py}
      finance/{returns.py,covariance.py,objective.py,backtest.py}
      solvers/{exact.py,annealing.py,xy_qaoa.py,penalty_qaoa.py,agp_experiment.py}
      metrics/{quality.py,resources.py}
      services/{runs.py,exports.py}
    tests/
  experiments/
    configs/
    results/
    notebooks/
  docs/
    methodology.md
    reproducibility.md
  scripts/
  README.md
  docker-compose.yml
```

### API sketch
- `GET /api/health`
- `GET /api/datasets`
- `POST /api/validate-data`
- `POST /api/runs` — config + dataset reference; returns run ID
- `GET /api/runs/{run_id}` — status and metrics
- `GET /api/runs/{run_id}/portfolio`
- `GET /api/runs/{run_id}/export` — config, metrics, selected assets, metadata

### Key tests
- Covariance symmetry and positive-semidefinite tolerance.
- Return/annualization calculations.
- Cardinality and objective correctness.
- Dicke-state support contains only Hamming-weight-K states.
- XY mixer conserves Hamming weight (numerical unit test).
- Exact solver matches objective optimum.
- API schema validation and deterministic synthetic dataset.
- Backtest chronology and transaction-cost accounting.

## 8. Roadmap
**Phase 0 — Reproducible core:** synthetic data, objective, exact enumeration, simulated annealing, tests, JSON exports.  
**Phase 1 — Quantum baseline:** Dicke state, XY mixer, simulator execution, circuit metrics, multiple seeds.  
**Phase 2 — Dashboard:** data diagnostics, solver comparison, run history, export bundle.  
**Phase 3 — Research extensions:** AGP/counterdiabatic terms, RMT ablations, CAF only with a mathematically explicit and reproducible definition.  
**Phase 4 — Hardware validation:** submit a small circuit to an available QPU; archive backend, job ID, calibration snapshot, shots, transpilation, and noise data.  
**Phase 5 — Financial robustness:** walk-forward backtests and stress tests with strict leakage and cost controls.

## 9. Master coding-agent prompt
The companion file `Q_FRONTIER_Coding_Agent_Master_Prompt.md` contains the complete build prompt, phased implementation instructions, stack, folder layout, testing requirements, and scientific guardrails.

## 10. References / source URLs supplied in the user's documents
The following are retained as source leads, not certified citations:
- https://iqc.devpost.com/
- https://iqc.devpost.com/rules
- https://intermountainquantum.org/
- https://aqora.io/challenges
- https://arxiv.org/html/2605.06858v1
- https://arxiv.org/html/2602.14827v1
- https://arxiv.org/html/2604.19832v1
- https://arxiv.org/pdf/2602.23976
- https://arxiv.org/html/2609.15708
- https://arxiv.org/pdf/2610.00736
- https://arxiv.org/abs/2504.06253
- https://arxiv.org/pdf/2510.11153
- https://arxiv.org/html/2509.01496v1
- https://arxiv.org/html/2509.18530
- https://arxiv.org/abs/2305.00905
- https://arxiv.org/html/2607.20168v1
- https://www.quantumrings.com/doc/
- https://pypi.org/project/QuantumRingsLib/
- https://quantum.ibm.com/
- https://docs.ionq.com/

**Bottom line:** build a small, fully reproducible constrained-optimization comparison first. A narrow, honest result with runnable code is more persuasive than a broad architecture supported by numbers that cannot yet be reproduced.
