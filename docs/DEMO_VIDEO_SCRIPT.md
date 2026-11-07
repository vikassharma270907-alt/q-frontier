# Q-FRONTIER: Demo Video Walkthrough Script (2:30 Target)
**Video Title:** Q-FRONTIER — Context-Aware Counterdiabatic Quantum Portfolio Optimization & Benchmarking  
**Target Duration:** 2 minutes 30 seconds  
**Recorded By:** Team Q-FRONTIER  
**Submission:** Intermountain Quantum Competition (IQC) 2026 — BYU Physics & Devpost  

---

### [0:00 - 0:25] Introduction & Competition Context
- **Screen:** Browser opened to `http://localhost:8000/`. The header displays the **Q-FRONTIER** logo, IQC 2026 badge, and active sponsor pills (Nasdaq, Quantum Rings, IonQ, Sandia, IBM Quantum, Classiq, BYU Physics).
- **Voiceover:**
  > *"Welcome to Q-FRONTIER, our submission for the 2026 Intermountain Quantum Competition at Brigham Young University. When tackling cardinality-constrained portfolio optimization for Nasdaq equities, NISQ algorithms face severe limitations: penalty terms leak measurement shots, static clustering loses cross-cluster risk, and unconstrained rebalancing destroys returns through turnover costs. Here is how Q-FRONTIER solves these challenges in a single unified workbench."*

---

### [0:25 - 0:50] Tab 1: Stage 1 RMT Spectral Denoising & Clustering
- **Screen:** Presenter clicks the **"RMT Spectral Denoising"** tab.
- **Visuals:** Shows the Marchenko-Pastur bound $\lambda_+$, the 3 partitioned clusters (max 4 qubits each), and the interactive Denoised Correlation Heatmap ($\mathcal{C}^\star$).
- **Voiceover:**
  > *"We begin in Stage 1 with real Nasdaq market data. We compute the Ledoit-Wolf shrinkage covariance and apply Random Matrix Theory Marchenko-Pastur filtering. Eigenvalues below lambda-plus represent market noise and are filtered out, preserving genuine economic structure. Our hardware-aware clustering algorithm then splits the 12-asset universe into 3 clusters of at most 4 qubits each, perfectly sized for near-term quantum processors."*

---

### [0:50 - 1:30] Tab 2: Stages 2 & 3 CCD-QAOA & QCL Volatility Sensor
- **Screen:** Presenter switches to the **"CCD-QAOA & QCL Engine"** tab.
- **Actions:**
  1. Points to the **QCL Volatility Sensor** readout showing predicted rough volatility (e.g. 21.8%) and dynamic risk aversion $q_t = 0.49$.
  2. Points to the 3-card comparison: Penalty-QAOA (26.9% AR, 26.7% leakage) vs Standard XY-QAOA (55.7% AR) vs **CCD-QAOA (95.7% AR, 100% feasibility)**.
  3. Clicks **"p = 2 (Optimal)"** and hits **"Run Quantum Rebalance"**. The animation updates live to 99.8% AR with the statevector chart rendering the exact optimal basis states.
- **Voiceover:**
  > *"In Stage 2, our 4-qubit Data-Reuploading QCL sensor reads four primitive market signals and dynamically tunes the portfolio risk aversion $q_t$. In Stage 3, we execute our Constrained Counterdiabatic QAOA solver. Look at this comparison: standard Penalty-QAOA leaks nearly 27% of all shots into invalid portfolio sizes. By initializing in exact Dicke states with complete-graph XY mixers, our solver achieves 100% feasibility with zero leakage. Adding 3-body Adiabatic Gauge Potential driving jumps the approximation ratio to 95.7% at depth 1, and over 99.7% at depth 2."*

---

### [1:30 - 2:00] Tab 3: Stage 4 Walk-Forward Backtest & Turnover Control
- **Screen:** Presenter navigates to the **"Walk-Forward Backtest"** tab.
- **Visuals:** The interactive Recharts line chart shows Q-FRONTIER outperforming the equal-weight benchmark net of 5 bps transaction costs. KPI cards highlight the Net Sharpe Ratio, Max Drawdown, and optimal continuous SLSQP weight allocations.
- **Voiceover:**
  > *"Stage 4 takes the quantum-selected asset subset and optimizes continuous weights for maximum Sharpe ratio via SLSQP. In our monthly walk-forward simulation, returns are evaluated strictly net of 5 basis points transaction fees. By incorporating our turnover continuity bonus kappa, Q-FRONTIER suppresses unnecessary rebalancing churn, beating the benchmark by over 25% cumulative return with significantly lower maximum drawdown."*

---

### [2:00 - 2:30] Tab 4: Hardware Transpilation Audit & Sandia Volumetric Heatmap
- **Screen:** Presenter switches to the **"Sandia & IonQ Benchmarks"** tab.
- **Visuals:** Shows IonQ Trapped-Ion (0 routing SWAPs) vs IBM Heavy-Hex (+18 SWAPs) and the full 2D Sandia Volumetric Benchmarking heatmap across Width ($w \in \{4, 6, 8, 12\}$) and Depth ($d \in \{1..5\}$).
- **Voiceover:**
  > *"Finally, we benchmark physical hardware topologies. On IonQ's trapped-ion architecture, all-to-all connectivity executes complete-graph mixers with zero routing SWAPs, while heavy-hex superconducting grids require up to 18 additional SWAPs. Following the methodology of Timothy Proctor and the team at Sandia National Laboratories, our 2D Volumetric Heatmap evaluates circuit capability across width and depth under noise. Q-FRONTIER is fully tested with 32 passing unit tests and a single-click Jupyter notebook. Thank you!"*

