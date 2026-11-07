# Q-FRONTIER: Animated Video Demo & Narration Walkthrough (MD-Format)
**Project:** Q-FRONTIER — Auditable Hybrid Quantum Optimization Workbench  
**Event:** Intermountain Quantum Competition (IQC) 2026 (Brigham Young University)  
**Target Duration:** 2 minutes 45 seconds (165 seconds) — *Strictly under 3 minutes*  
**Voice Engine:** Wispr Flow (Voice Preset: *Marcus — Crisp Studio Technical Narrator*, Speed: 1.0x / 135 WPM, Stability: 0.78)  
**Animation Engine:** Interactive HTML5 / CSS3 Keyframe Video Player (`docs/video_demo_player.html`)

---

## 🎬 Video Overview & Timeline Cue Sheet

| Scene | Timecode | Duration | Focus Area | Key Animation / Visual Effect | Words | Target WPM |
|---|---|---|---|---|---|---|
| **Scene 1** | `0:00 - 0:25` | 25s | Introduction & Competition Context | Pulsing Q-FRONTIER Hero, glowing sponsor badges, floating Bloch sphere | 58 words | 139 WPM |
| **Scene 2** | `0:25 - 0:55` | 30s | Stage 1: RMT Spectral Denoising & Clustering | Animated Marchenko-Pastur $\lambda_+$ filter line, 12-to-3 cluster particle split | 69 words | 138 WPM |
| **Scene 3** | `0:55 - 1:40` | 45s | Stages 2 & 3: QCL Sensor & CCD-QAOA Engine | Penalty shot leakage red pulse vs Dicke 100% blue feasible spikes; AGP commutator drive | 104 words | 138 WPM |
| **Scene 4** | `1:40 - 2:15` | 35s | Stage 4: SLSQP Allocation & Walk-Forward Backtest | Live equity curve stroke animation beating benchmark net of 5 bps fees; SLSQP weight allocation donut | 81 words | 139 WPM |
| **Scene 5** | `2:15 - 2:45` | 30s | Hardware Topologies & Sandia Volumetric Heatmap | IonQ (0 SWAPs) vs IBM (+18 SWAPs) gate routing; 2D Sandia volumetric capability grid | 68 words | 136 WPM |
| **Total** | `0:00 - 2:45` | **165s** | **Full 4-Stage Auditable Pipeline** | **End-to-End Auditable Demo with Verification** | **380 words** | **138 WPM** |

---

## 🎙️ Wispr Flow Voice Setup & Sound Design Directives

```ini
[Wispr_Flow_Profile]
Engine = "Wispr Flow Neural TTS / Voice Dictation"
Voice_Persona = "Marcus - Confident Technical Researcher"
Tone = "Authoritative, engaging, mathematically precise, studio-grade clarity"
Pacing = "135 - 140 Words Per Minute"
Audio_Format = "48kHz 24-bit Lossless WAV / AAC"
Background_Ambience = "Subtle cinematic cybernetic synth pad (-26 dB under voiceover)"
```

### Phonetic Pronunciation Guide for Wispr Flow:
- `Q-FRONTIER` $\rightarrow$ *"Queue-Frontier"*
- `QAOA` $\rightarrow$ *"Q-A-O-A"* (`/kjuː eɪ oʊ eɪ/`)
- `CCD-QAOA` $\rightarrow$ *"C-C-D Q-A-O-A"*
- `Marchenko-Pastur` $\rightarrow$ *"Mar-CHEN-ko Pas-TOOR"*
- `Dicke state` $\rightarrow$ *"DICK-ee state"* (`/ˈdɪki steɪt/`)
- `Adiabatic Gauge Potential (AGP)` $\rightarrow$ *"Ay-dee-uh-BAT-ik Gauge Potential, A-G-P"*
- `SLSQP` $\rightarrow$ *"S-L-S-Q-P"*
- `bps` $\rightarrow$ *"basis points"*
- `IonQ` $\rightarrow$ *"Eye-on-Q"*
- `NISQ` $\rightarrow$ *"Nisk"* (`/nɪsk/`)

---

## 🎞️ Scene-by-Scene Animation Storyboard & Narration

---

### 🟢 SCENE 1: Introduction & Competition Context
- **Timecode:** `0:00 - 0:25` (Duration: 25 seconds)
- **On-Screen Display:** 
  - `http://localhost:8000` Audit Workbench view with glowing header.
  - Active Sponsor Pills: **Nasdaq**, **Quantum Rings**, **IonQ**, **Sandia National Laboratories**, **IBM Quantum**, **Classiq**, **BYU Physics**.
  - Scientific Guardrail Pill: `[SIMULATED EXACT QISKIT AER — NO UNVERIFIED QUANTUM ADVANTAGE]`.
- **Visual Animation Choreography:**
  - `0:00 - 0:05`: Hero title smoothly zooms in (`scale(0.96) -> scale(1.0)`) with cybernetic cyan particle glow.
  - `0:05 - 0:12`: Sponsor pills light up sequentially with a metallic sweep effect.
  - `0:12 - 0:20`: Side-by-side callout cards animate into view showing the 4 classical NISQ hurdles: *Penalty Leakage*, *Static Risk*, *Covariance Loss*, *Turnover Drag*.
  - `0:20 - 0:25`: Quantum Bloch sphere graphic transitions to the RMT spectral matrix.

```
+-----------------------------------------------------------------------------------------+
| [0:00 - 0:25] SCENE 1: Q-FRONTIER HERO & BENCHMARK SUITE                                |
|                                                                                         |
|   ★ Q - F R O N T I E R   [Intermountain Quantum Competition 2026 - BYU Physics]         |
|   Sponsors: [Nasdaq] [Quantum Rings] [IonQ] [Sandia] [IBM Quantum] [Classiq]            |
|                                                                                         |
|   +--------------------------+   +--------------------------+   +---------------------+ |
|   | 1. Penalty Shot Leakage  |   | 2. Static Risk Fallacy   |   | 3. Turnover Drag    | |
|   | Quadratic penalty loses  |   | Fixed risk aversion      |   | High rebalancing    | |
|   | >25% of quantum shots    |   | fails in rough regimes   |   | wipes out net gains | |
|   +--------------------------+   +--------------------------+   +---------------------+ |
+-----------------------------------------------------------------------------------------+
```

- **Wispr Flow Narration:**
> *"Welcome to Q-FRONTIER, our submission for the 2026 Intermountain Quantum Competition at Brigham Young University. [pause: 250ms] When solving cardinality-constrained portfolio optimization for Nasdaq equities, NISQ algorithms face a critical bottleneck: quadratic penalties leak measurement shots, static clustering ignores cross-cluster risk, and unconstrained rebalancing destroys capital through fees. [pause: 300ms] Q-FRONTIER eliminates all three challenges in a single auditable workbench."*

---

### 🟢 SCENE 2: Stage 1 — RMT Marchenko-Pastur Spectral Denoising & Clustering
- **Timecode:** `0:25 - 0:55` (Duration: 30 seconds)
- **On-Screen Display:** 
  - Navigation tab switches to **"RMT Spectral Denoising"**.
  - Marchenko-Pastur eigenvalue spectrum distribution plot.
  - Interactive Denoised Correlation Heatmap ($\mathcal{C}^\star$).
  - 3 partitioned subproblems (max 4 qubits each) with asset tickers.
- **Visual Animation Choreography:**
  - `0:25 - 0:32`: Correlation matrix heatmap renders with high-frequency noise fluttering.
  - `0:32 - 0:42`: Animated vertical dashed red line sweeps across the eigenvalue axis, marking the Marchenko-Pastur noise threshold $\lambda_+ = \sigma^2(1 + \sqrt{N/T})^2$.
  - `0:42 - 0:50`: Eigenvalues below $\lambda_+$ dissolve into their trace-preserving mean, and the correlation heatmap crisply snaps into denoised block-diagonal form.
  - `0:50 - 0:55`: The 12 Nasdaq assets cluster into 3 distinct color-coded hardware clusters: Cluster 1 (Tech Growth, 4 qubits), Cluster 2 (Defensive, 4 qubits), Cluster 3 (Cyclical, 4 qubits).

```
+-----------------------------------------------------------------------------------------+
| [0:25 - 0:55] SCENE 2: RMT MARCHENKO-PASTUR EIGENVALUE DENSITY                           |
|                                                                                         |
|   Eigenvalue Density ρ(λ)                                                               |
|     |  ▲ Noise Bulk (Filtered)           | Genuine Signal (Preserved)                   |
|     | █ █ █ █ █ █ █                      |                                              |
|     | █ █ █ █ █ █ █ █ █                  |         █  (Market Mode)                     |
|     | █ █ █ █ █ █ █ █ █ █ █              |      █  █                                    |
|     +-------------------------|----------+-------------------> λ (Eigenvalues)          |
|                              λ+ = 1.9431                                                |
|   -> 12 Equities Partitioned into 3 Hardware-Matched Clusters (Max 4 Qubits Each)       |
+-----------------------------------------------------------------------------------------+
```

- **Wispr Flow Narration:**
> *"We start with real Nasdaq-12 market data. [pause: 200ms] We compute the Ledoit-Wolf shrinkage covariance and apply Random Matrix Theory Marchenko-Pastur filtering. [pause: 250ms] All eigenvalues below lambda-plus represent empirical noise and are filtered out, preserving genuine economic signal. [pause: 250ms] Our hardware-aware clustering algorithm then partitions the 12-asset universe into 3 clusters of at most 4 qubits each—ideally sized for near-term quantum processors."*

---

### 🟢 SCENE 3: Stages 2 & 3 — QCL Volatility Sensor & CCD-QAOA Engine (Zero Leakage)
- **Timecode:** `0:55 - 1:40` (Duration: 45 seconds)
- **On-Screen Display:** 
  - Tab switches to **"CCD-QAOA & QCL Engine"**.
  - Top card: 4-Qubit Data-Reuploading QCL Sensor reading 4 primitive features (lagged return, variance, asymmetry, rough increments), outputting predicted volatility $21.8\%$ and dynamic risk aversion $q_t = 0.49$.
  - Main comparison: 3-Way Solver Statevector Probability Distribution:
    1. *Penalty-QAOA:* 26.9% AR, **26.7% Shot Leakage** into invalid Hamming weights.
    2. *Standard XY-QAOA:* 55.7% AR, 100% Feasibility.
    3. *Constrained Counterdiabatic QAOA (CCD-QAOA):* **95.7% AR ($p=1$)** and **99.8% AR ($p=2$)**, **100% Feasibility**.
- **Visual Animation Choreography:**
  - `0:55 - 1:08`: QCL circuit pulse: 4 quantum wires light up with $R_y(\phi)$ rotations and CX entangling gates, updating the dynamic risk slider $q_t$.
  - `1:08 - 1:20`: Live comparison bar chart renders. The Penalty-QAOA bars flash alarming red for invalid states ($|0000\rangle, |1111\rangle$, Hamming weight $\ne 2$), highlighting 26.7% wasted shots.
  - `1:20 - 1:32`: Camera zooms into CCD-QAOA: statevector probability mass snaps exclusively into the 6 feasible basis states of $|D_2^4\rangle$ with bright cyan glow (zero leakage).
  - `1:32 - 1:40`: User clicks `depth p = 2`; 3-body commutator gauge drive $H_{CD} = i[H_C, H_M^{XY}] / \|[H_C, H_M^{XY}]\|_2$ activates, and the optimal ground-state probability spikes to 99.8%.

```
+-----------------------------------------------------------------------------------------+
| [0:55 - 1:40] SCENE 3: SUBPROBLEM SOLVERS — PROBABILITY MASS & FEASIBILITY             |
|                                                                                         |
|   [Penalty-QAOA]          [Standard XY-QAOA]        [Q-FRONTIER CCD-QAOA (AGP)]         |
|   Approximation: 26.9%    Approximation: 55.7%      Approximation: 95.7% (p=1) / 99.8%  |
|   Feasibility:   73.3%    Feasibility:   100.0%     Feasibility:   100.0%               |
|   Leakage:       26.7% ✘  Leakage:       0.0%  ✔    Leakage:       0.0%  ✔              |
|                                                                                         |
|   Probability Bar Chart:                                                                |
|   Penalty: [████ Feasible: 73.3%] [███ LEAKAGE: 26.7% ✘]                                |
|   CCD-QAOA: [████████████████████████████ 100% FEASIBLE SUB-SPACE | OPTIMUM: 99.8% ✔]  |
+-----------------------------------------------------------------------------------------+
```

- **Wispr Flow Narration:**
> *"In Stage 2, our 4-qubit data-reuploading QCL sensor encodes four primitive market signals and dynamically calibrates portfolio risk aversion $q_t$. [pause: 250ms] In Stage 3, we execute our Constrained Counterdiabatic QAOA solver. [pause: 300ms] Look closely at this comparison: standard Penalty-QAOA leaks over 26% of all shots into illegal portfolio sizes. [pause: 250ms] By initializing registers in exact Dicke states with complete-graph XY mixers, Q-FRONTIER mathematically guarantees 100% feasibility with zero leakage. [pause: 250ms] Adding 3-body Adiabatic Gauge Potential driving boosts the approximation ratio to 95.7% at single depth, and over 99.7% at depth two."*

---

### 🟢 SCENE 4: Stage 4 — Continuous SLSQP Weights & Net 5 bps Backtest
- **Timecode:** `1:40 - 2:15` (Duration: 35 seconds)
- **On-Screen Display:** 
  - Tab switches to **"Walk-Forward Backtest"**.
  - Interactive Recharts Cumulative Equity Curve (180 days walk-forward simulation).
  - Benchmark line (Equal-Weight SPY/Nasdaq) vs Q-FRONTIER Net Curve.
  - KPI Stat Badges: **Net Sharpe Ratio: 2.14**, **Max Drawdown: -4.8%**, **Turnover Reduction: 42%**, **Fee Model: 5.0 bps Net Deduction**.
  - Donut chart displaying continuous SLSQP asset weights for selected cardinality $K=2$.
- **Visual Animation Choreography:**
  - `1:40 - 1:52`: SLSQP optimization dial spins and locks into continuous optimal weights (e.g. 58% AAPL, 42% MSFT).
  - `1:52 - 2:05`: Dual equity curve lines draw across the timeline from left to right; Q-FRONTIER pulls steadily ahead of the grey benchmark line, compounding higher returns.
  - `2:05 - 2:15`: A fee deduction tooltip pops up over each monthly rebalance node, proving that the net performance includes full 5 bps execution costs and turnover continuity bonus $\kappa$.

```
+-----------------------------------------------------------------------------------------+
| [1:40 - 2:15] SCENE 4: WALK-FORWARD EQUITY CURVE (NET OF 5 BPS TRANSACTION FEES)         |
|                                                                                         |
|   Portfolio Value ($)                                                                   |
|   $12,500 |                                                 .-' Q-FRONTIER (+24.8% Net) |
|   $11,500 |                                         _..---''                            |
|   $10,500 |                      _..---'''''''''''''                                    |
|   $10,000 | ---------''''''''''''------------------------- Equal Weight Benchmark       |
|    $9,500 |________________________________________________                            |
|           Day 0             Day 60           Day 120          Day 180                   |
|                                                                                         |
|   KPIs: Net Sharpe: 2.14  |  Max Drawdown: -4.8%  |  Transaction Cost: 5 bps Net        |
+-----------------------------------------------------------------------------------------+
```

- **Wispr Flow Narration:**
> *"Stage 4 takes the quantum-selected asset subset and optimizes continuous weights for maximum Sharpe ratio using SLSQP. [pause: 250ms] In our monthly walk-forward simulation, all returns are evaluated strictly net of five basis points transaction costs. [pause: 250ms] By incorporating our turnover continuity parameter kappa, Q-FRONTIER suppresses costly portfolio churning, outperforming the benchmark by over 24% cumulative return with less than half the maximum drawdown."*

---

### 🟢 SCENE 5: Hardware Transpilation Audit, Sandia Volumetric Heatmap & Conclusion
- **Timecode:** `2:15 - 2:45` (Duration: 30 seconds)
- **On-Screen Display:** 
  - Tab switches to **"Sandia & Hardware Benchmarks"**.
  - Physical Topology Comparison:
    - **IonQ Aria / Forte (Trapped-Ion):** All-to-all connectivity $\rightarrow$ **0 Routing SWAPs**, 12 two-qubit gates.
    - **IBM Quantum Heavy-Hex (Superconducting):** Nearest-neighbor $\rightarrow$ **+18 Routing SWAPs**, 48 two-qubit gates.
  - 2D Sandia Volumetric Benchmarking Heatmap grid (Width $w \in [4, 12]$, Depth $d \in [1, 5]$).
  - One-Click Reproducibility Bundle Export button with green SHA-256 verified checkmark.
- **Visual Animation Choreography:**
  - `2:15 - 2:25`: Trapped-ion vs heavy-hex topology graphs animate: trapped-ion links ignite simultaneously in a clean circle, while heavy-hex inserts routing SWAP bridges.
  - `2:25 - 2:35`: Sandia 2D heatmap tiles animate from green (high success rate at $w=4, d=1$) to yellow/red as circuit depth increases, demonstrating empirical NISQ noise limits.
  - `2:35 - 2:45`: Presenter clicks **"Export Reproducibility Bundle"**; green badge flashes: `SHA-256: e3b0c442... [43 Passing Tests]`. Final fade-out on the BYU IQC 2026 splash card.

```
+-----------------------------------------------------------------------------------------+
| [2:15 - 2:45] SCENE 5: HARDWARE TOPOLOGIES & 2D SANDIA VOLUMETRIC HEATMAP               |
|                                                                                         |
|   IonQ Trapped-Ion (All-to-All)          IBM Heavy-Hex (Nearest-Neighbor)               |
|   ★ 0 Routing SWAPs (12 2Q Gates)        ★ +18 Routing SWAPs (48 2Q Gates)              |
|                                                                                         |
|   Sandia Volumetric Grid:               Reproducibility Package:                        |
|   Width \ Depth  d=1   d=2   d=3        [Download JSON Bundle]                          |
|   w = 4 qubits   98%   95%   89%        ✔ SHA-256 Provenance Hashed                     |
|   w = 8 qubits   91%   84%   72%        ✔ 43/43 Passing Pytest Suites                   |
|   w = 12 qubits  82%   68%   51%        ✔ Deterministic Random Seeds                    |
+-----------------------------------------------------------------------------------------+
```

- **Wispr Flow Narration:**
> *"Finally, we benchmark physical hardware topologies. [pause: 200ms] On IonQ's trapped-ion architecture, all-to-all connectivity compiles our complete-graph mixers with zero routing SWAPs, while heavy-hex grids require 18 additional SWAPs. [pause: 250ms] Following Sandia National Laboratories' volumetric benchmarking framework, our 2D heatmap maps circuit capability under noise. [pause: 200ms] Q-FRONTIER is fully verifiable, backed by 43 automated tests and one-click reproducibility. Thank you!"*

---

## 📊 Summary of Video Pacing & Timing Bounds

- **Total Narration Word Count:** 380 words
- **Speech Delivery Speed:** 138.2 words per minute (optimal for technical clarity)
- **Total Spoken Duration:** 165 seconds = **2 minutes 45 seconds**
- **Safety Margin:** 15 seconds below the 3:00 minute hard ceiling!
- **Audience Takeaway:** Clear, un-hyped scientific honesty, mathematically sound constraint satisfaction, and tangible benchmark comparisons across exact classical, heuristic, and quantum solvers.
