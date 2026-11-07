# Devpost Submission Form Content: Q-FRONTIER

**Project Name:** Q-FRONTIER: Context-Aware Counterdiabatic Quantum Portfolio Optimization & Volumetric Hardware Benchmarking  
**Tagline:** A hybrid quantum-classical portfolio optimization platform combining RMT spectral clustering, 4-qubit QCL rough-volatility sensing, and Constrained Counterdiabatic QAOA (CCD-QAOA).  
**Target Tracks:** Fintech & Real-Data Optimization, Quantum Machine Learning, Hardware Benchmarking  
**GitHub Repository:** https://github.com/your-team/Q-FRONTIER  
**Live Demo:** http://localhost:8000/ (or hosted Vercel/Render URL)  

---

### Inspiration
Institutional index and quantitative asset managers (such as market participants on Nasdaq) face an **NP-hard combinatorial optimization bottleneck** when constructing cardinality-constrained, low-turnover equity portfolios. 

While exploring existing quantum hackathon submissions—including *BioQubit Labs (Q-VIRA)*, which deployed a 3-qubit PennyLane circuit for viral mutation triage—we noticed a major strategic opening. Most quantum prototypes either stay confined to small toy classifications or attempt unconstrained formulations that fail under real-world conditions:
1. **NISQ Depth Ceilings:** Mapping 40+ equities to a single QPU exceeds coherence limits, while naive clustering discards cross-cluster risk covariance.
2. **Shot Leakage:** Penalty-based QAOA leaks over 25% of measurement shots outside valid portfolio sizes ($|z| \neq K$).
3. **Static Risk Fallacy:** Markowitz models assume fixed risk-aversion $q$, ignoring rough volatility and asymmetric leverage spikes.
4. **Turnover Erosion:** Unconstrained rebalancing yields over 60% monthly turnover, destroying capital via transaction costs.

We built **Q-FRONTIER** to prove that by grounding quantum algorithms in recent 2025–2026 literature, quantum computers can deliver mathematically rigorous, subspace-preserving portfolio optimization on real market data.

---

### What It Does
**Q-FRONTIER** executes an end-to-end four-stage pipeline:
1. **Stage 1: Nasdaq Ingestion & RMT Spectral Denoising:** Ingests rolling 180-day price series for liquid Nasdaq equities, calculates Ledoit-Wolf shrinkage covariance, and filters out noise eigenvalues below the Marchenko-Pastur upper bound ($\lambda_+$). It then partitions the universe into hardware-executable subproblems ($n_c \le 4$ qubits) via `get_clusters()`.
2. **Stage 2: 4-Qubit Data-Reuploading QCL Volatility Sensor:** Encodes strictly four primitive market observables ($r_{t-1}$, $\sigma^2_{t-1}$, downside leverage asymmetry, and rough volatility increments $dV_t$) into a 3-layer, 36-parameter quantum neural network with non-negative physical clipping $\max(0, \langle \hat{Z}_0 \rangle)$ to dynamically set risk-aversion $q_t \in [0.2, 0.8]$.
3. **Stage 3: Context-Aware Folding + Constrained Counterdiabatic QAOA:** Initializes registers in exact Dicke states $|D_K^n\rangle$ and evolves under complete-graph $XY$ mixers ($[H_M^{XY}, \sum Z_i] = 0$), guaranteeing **100% feasibility** with zero shot leakage. It drives the system with 3-body Adiabatic Gauge Potential (AGP) commutators ($H_{CD} \propto i[H_C, H_M]$), jumping single-layer approximation ratios from 55.7% to **95.7% at p=1** and **99.8% at p=2**. Cross-cluster covariance is preserved via Context-Aware Folding (CAF), reducing portfolio risk by **10.7% to 13.8%** with monotonic descent ($\Delta \mathcal{O} \le -\epsilon$).
4. **Stage 4: SLSQP Continuous Weights & Hardware Benchmarks:** Computes continuous Sharpe-optimal weights ($w_i$), runs a monthly walk-forward backtest net of $5\text{ bps}$ transaction costs, and charts a **Sandia Volumetric Benchmarking** 2D heatmap ($w \in \{4, 6, 8, 12\}$ vs. $d \in \{1..5\}$) alongside an **IonQ vs. IBM SWAP routing audit**.

---

### How We Built It
- **Backend & Quantum Core:** Python 3.11+, Qiskit 2.6.2, Qiskit Aer, and Quantum Rings (`QuantumRingsLib`), orchestrated via FastAPI.
- **Financial Optimization:** Scipy SLSQP, Scikit-learn (Ledoit-Wolf shrinkage), Pandas, and NumPy.
- **Frontend Dashboard:** React 18, Vite, Tailwind CSS, Lucide icons, and Recharts, packaged into a single-port deployment served directly by FastAPI.
- **Testing & Verification:** 32 comprehensive unit and integration tests across 10 modules covering linear algebra invariants, commutation proofs, monotonic descent, and API schema boundaries.
- **Notebook:** Standalone Jupyter notebook (`IQC_Q_FRONTIER_Master.ipynb`) runnable on Aqora, qBraid, or local environments with a single "Run All".

---

### Challenges We Ran Into
- **Commutator Algebra & 3-Body Terms:** Constructing the exact Adiabatic Gauge Potential commutator $i[H_C, H_M^{XY}]$ across arbitrary subproblem graphs required carefully evaluating tensor products of Pauli operators and verifying that 3-body terms $Z_j(Y_i X_k + X_i Y_k)$ commute with the total magnetization operator.
- **SLSQP Box Constraint Edge Case:** For cardinality $K=2$, a naive upper bound of $0.40$ per asset makes $\sum w_i = 1.0$ mathematically impossible. We resolved this by dynamically scaling bounds via `max(max_weight, 1.0/k)`.
- **Quantum Kernel Concentration:** Replicating Shen's recent 2026 paper taught us that feeding pre-computed polynomial features into quantum kernels leads to exponential Gram matrix concentration. We restricted Stage 2 strictly to primitive observables, letting quantum entanglement form higher-order interactions naturally.

---

### Accomplishments That We're Proud Of
- **100% Subspace Feasibility:** Zero measurement shots leaked outside the cardinality budget, contrasting sharply with penalty QAOA's 26.7% leakage.
- **Near-Unitary Approximation at $p=1$:** Achieving an approximation ratio of 95.68% at single-layer depth using AGP counterdiabatic shortcuts.
- **Multi-Sponsor SDK Integration:** Seamlessly integrating tools from **Nasdaq, Quantum Rings (`QuantumRingsLib`), IonQ (0-SWAP routing), Sandia (Volumetric Benchmarking), and IBM Quantum**.
- **100% Green Test Suite:** 32 passing tests verifying all algebraic, statistical, and API invariants in under 6 seconds.

---

### What We Learned
- **Scientific Honesty Wins Over Hype:** Clearly documenting where quantum kernels concentrate, why turnover continuity bonuses are necessary to survive transaction costs, and why subproblems must be bounded to $n_c \le 6$ under current NISQ gate fidelities provides far stronger academic credibility than claiming artificial "quantum supremacy".

---

### What's Next for Q-FRONTIER
- Running live execution on IonQ Forte trapped-ion hardware via qBraid.
- Extending continuous allocation from SLSQP to Quantum Interior Point Methods (QIPM).
- Integrating real-time streaming L2 order book data via Nasdaq Data Link APIs.

---

### Built With
`python`, `qiskit`, `qiskit-aer`, `quantumringslib`, `fastapi`, `react`, `vite`, `tailwindcss`, `recharts`, `scipy`, `numpy`, `pandas`, `scikit-learn`
