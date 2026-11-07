# Q-FRONTIER: Mathematical Methodology & Architectural Specification

**Version:** 2.0.0  
**Domain:** Cardinality-Constrained Quantum & Classical Portfolio Optimization  
**Audience:** Researchers, Auditors, and Competition Reviewers  

---

## 1. Problem Formulation

### 1.1 Cardinality-Constrained Binary Portfolio Selection
Portfolio selection is formulated as a combinatorial 0-1 quadratic program over an equity universe of $N$ assets with a hard cardinality constraint $K$ ($K < N$):

$$\min_{x \in \{0, 1\}^N} \quad f(x) = \lambda \cdot x^T \Sigma x - (1 - \lambda) \cdot \mu^T x - \kappa \cdot x_{\text{prev}}^T x$$

$$\text{subject to} \quad \sum_{i=1}^N x_i = K$$

Where:
- $x = [x_1, \dots, x_N]^T \in \{0, 1\}^N$ is the binary asset selection indicator vector ($x_i = 1$ if asset $i$ is included in the portfolio, $0$ otherwise).
- $\Sigma \in \mathbb{R}^{N \times N}$ is the symmetric, positive semi-definite (PSD) annualized asset return covariance matrix.
- $\mu \in \mathbb{R}^N$ is the vector of annualized expected asset returns.
- $\lambda \in [0, 1]$ is the user-controlled risk-aversion parameter ($\lambda = 1.0$ represents pure risk minimization; $\lambda = 0.0$ represents pure expected return maximization).
- $\kappa \ge 0$ is an optional turnover-dampening continuity bonus against the previous period selection $x_{\text{prev}}$.
- $K \in \{1, \dots, N-1\}$ is the exact target number of assets to select.

---

## 2. Statistical Covariance Estimators

Accurate estimation of $\Sigma$ is critical to prevent Markowitz error-maximization:

### 2.1 Sample Covariance
For centered return matrix $\tilde{R} \in \mathbb{R}^{T \times N}$ across $T$ observations:
$$\Sigma_{\text{sample}} = \frac{252}{T - 1} \tilde{R}^T \tilde{R}$$

### 2.2 Ledoit–Wolf Analytical Shrinkage
To regularize ill-conditioned empirical covariance when $N/T$ is significant, Ledoit–Wolf shrinkage shrinks the sample covariance toward a constant-correlation target $F$:
$$\Sigma_{\text{LW}} = (1 - \alpha) \Sigma_{\text{sample}} + \alpha F$$
where $\alpha \in [0, 1]$ is analytically optimal under the Frobenius norm.

### 2.3 Random Matrix Theory (RMT) Marchenko–Pastur Spectral Denoising
Under the null hypothesis that returns are uncorrelated random noise, the eigenvalues of empirical correlation matrix $C$ follow the Marchenko–Pastur distribution with upper spectral edge:
$$\lambda_+ = \sigma^2 \left(1 + \sqrt{\frac{N}{T}}\right)^2$$
Eigenvalues $\lambda_i \le \lambda_+$ represent market noise; eigenvalues $\lambda_i > \lambda_+$ reflect genuine macroeconomic market factors. RMT denoising replaces noise eigenvalues with their trace-preserving mean:
$$\tilde{\lambda}_i = \begin{cases} \lambda_i, & \text{if } \lambda_i > \lambda_+ \\ \frac{1}{|I_{\text{noise}}|} \sum_{j \in I_{\text{noise}}} \lambda_j, & \text{if } \lambda_i \le \lambda_+ \end{cases}$$
The denoised covariance $\Sigma_{\text{RMT}}$ is reconstructed from $\tilde{C}$ and asset volatilities.

---

## 3. Quantum Subspace Mapping & Circuit Solvers

### 3.1 Mapping Binary Variables to Qubit Pauli Operators
Binary variables $x_i \in \{0, 1\}$ are mapped to Pauli $Z$ operators using the standard projection:
$$x_i = \frac{I - Z_i}{2}$$
Substituting this into the quadratic objective yields a diagonal Ising Cost Hamiltonian:
$$H_C = \sum_{i=1}^N h_i Z_i + \sum_{i < j}^N J_{ij} Z_i Z_j + C_{\text{shift}} I$$
For computational basis state $|b\rangle = |b_1 \dots b_N\rangle$, the eigenvalue is exactly the classical objective:
$$\langle b | H_C | b \rangle = f(b)$$

### 3.2 Dicke State Feasible Initializer
Standard QAOA prepares equal superposition $|+\rangle^{\otimes N}$, which spans all $2^N$ states with Hamming weights ranging from $0$ to $N$. In contrast, Q-FRONTIER initializes the register in the exact Dicke state $|D_K^N\rangle$:
$$|D_K^N\rangle = \frac{1}{\sqrt{\binom{N}{K}}} \sum_{\substack{x \in \{0, 1\}^N \\ \sum x_i = K}} |x\rangle$$
This confines $100\%$ of the initial probability amplitude strictly within the feasible subspace.

### 3.3 Complete-Graph XY Mixer
To evolve without leaking probability amplitude into infeasible Hamming-weight sectors, we use the complete-graph XY mixer Hamiltonian:
$$H_M^{XY} = \sum_{i < j}^N (X_i X_j + Y_i Y_j)$$
**Mathematical Proof of Subspace Preservation:**
$$[X_i X_j + Y_i Y_j, Z_i + Z_j] = 0$$
Summing over all pairs yields:
$$\left[H_M^{XY}, \sum_{k=1}^N Z_k\right] = 0$$
Because the total magnetization (Hamming weight operator) commutes with $H_M^{XY}$, any state initialized in the feasible subspace remains in that subspace under unitary evolution $e^{-i \beta H_M^{XY}}$.

### 3.4 Counterdiabatic AGP Shortcut (CCD-QAOA)
At shallow circuit depths ($p=1, 2$), standard QAOA is prone to diabatic transitions when energy levels approach avoided crossings. The Adiabatic Gauge Potential (AGP) generator introduces a counterdiabatic driving term:
$$H_{CD} = \frac{i [H_C, H_M^{XY}]}{\|[H_C, H_M^{XY}]\|_2}$$
The state is evolved under the modified unitary:
$$U(\gamma, \beta, \alpha) = \prod_{l=1}^p e^{-i \alpha_l H_{CD}} e^{-i \beta_l H_M^{XY}} e^{-i \gamma_l H_C}$$
This variational drive suppresses non-adiabatic leakage and boosts the ground-state approximation ratio without requiring deep circuits.

### 3.5 Penalty-QAOA Baseline (Unconstrained Transverse Mixer)
For rigorous comparison, Q-FRONTIER also implements the standard unconstrained baseline:
$$H_{\text{pen}} = H_C + \rho \left(\sum_{i=1}^N \frac{I - Z_i}{2} - K\right)^2, \quad H_M^X = \sum_{i=1}^N X_i$$
Because $[H_M^X, \sum Z_i] \ne 0$, probability amplitude leaks into infeasible states, directly illustrating the advantage of constraint-preserving mixers.

---

## 4. Classical Benchmarks

### 4.1 Exact Combinatorial Enumeration (Ground Truth)
For $N \le 16$, Q-FRONTIER evaluates all $\binom{N}{K}$ candidate binary vectors. It identifies:
- Ground truth minimum energy $E_{\min}$
- Exact worst feasible energy $E_{\max}$
- Optimal asset selection set $x^*$

### 4.2 Simulated Annealing Heuristic
To test against a strong classical heuristic, Simulated Annealing explores the feasible subspace using pairwise index swaps:
1. In each step, an active asset $i \in \{x=1\}$ and inactive asset $j \in \{x=0\}$ are randomly chosen and swapped.
2. The change in energy $\Delta E = f(x') - f(x)$ is computed.
3. The move is accepted if $\Delta E < 0$, or with Metropolis probability $P = \exp(-\Delta E / T)$ if $\Delta E \ge 0$.
4. Temperature cools according to geometric schedule $T_{k+1} = \eta T_k$.
5. Executed over multiple seeds to report median and interquartile range (IQR).

---

## 5. Standardized Evaluation Metrics

| Metric | Formula | Meaning |
|---|---|---|
| **Feasibility Rate** | $\sum_{x: \sum x_i = K} P(x)$ | Percentage of measured shots satisfying exactly $K$ assets |
| **Approximation Ratio (AR)** | $\frac{E_{\max} - \langle H_C \rangle}{E_{\max} - E_{\min}}$ | Solution quality normalized in $[0, 1]$ relative to exact optimum |
| **Optimal Probability $P(\text{opt})$** | $P(x = x^*)$ | Probability of sampling the exact ground truth portfolio |
| **Circuit Depth** | Transpiled layer count | Computational depth before decoherence |
| **Two-Qubit Gates** | CNOT / CX count | Entangling gate overhead |

---

## 6. Two-Stage Continuous Allocation & Backtesting

Following discrete asset selection $x^*$, continuous capital allocation weights $w \in \mathbb{R}^K$ are determined using Sequential Least Squares Quadratic Programming (SLSQP):

$$\max_{w \ge 0} \quad \frac{w^T \mu_S - r_f}{\sqrt{w^T \Sigma_S w}} \quad \text{s.t.} \quad \sum_{i=1}^K w_i = 1, \quad w_{\min} \le w_i \le w_{\max}$$

The resulting portfolio is evaluated through out-of-sample chronological walk-forward simulation:
- Rebalancing frequency: 21 trading days (monthly).
- Transaction cost deduction: 5 basis points ($0.0005$) per unit of turnover:
  $$\text{Fee}_t = 0.0005 \times \sum_{i=1}^N |w_{i, t} - w_{i, t^-}|$$
- Realized metrics: Annualized Return, Annualized Volatility, Net Sharpe Ratio, Maximum Drawdown.

---

## 7. Scientific & Financial Disclaimers

1. **Simulation-Only Execution:** All quantum results generated by Q-FRONTIER are produced via numerical statevector simulation. No claims of physical QPU supremacy or advantage are asserted.
2. **Research & Education Prototype:** This software is designed for academic benchmarking and algorithmic research. It does not constitute financial, investment, or trading advice.
