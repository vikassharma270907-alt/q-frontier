"""
Appends Section 9 (GNN Mixer), Section 10 (Conformal UQ), and Section 11 (Crisis Stress-Testing)
to notebooks/IQC_Q_FRONTIER_Master.ipynb if not already present.
"""

import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
nb_path = root_dir / "notebooks" / "IQC_Q_FRONTIER_Master.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Check if Section 9 is already present
has_gnn = any("Geometric Quantum ML" in "".join(c.get("source", [])) for c in nb["cells"])

if not has_gnn:
    new_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9. Geometric Quantum ML: GNN-Adaptive Sparsified XY Mixers (GQML)\n",
                "\n",
                "Inspired by Graph Attention Networks and Minimum Spanning Trees in financial ML, ",
                "this solver sparsifies the mixer Hamiltonian to the active topological backbone:\n",
                "$$\\hat{H}_M^{\\text{GNN}} = \\sum_{(i,j) \\in \\mathcal{E}_{\\text{GNN}}} w_{ij} (X_i X_j + Y_i Y_j)$$\n",
                "cutting two-qubit CNOT depth by 50%–75% while mathematically preserving 100% subspace feasibility.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from app.solvers.gnn_mixer import GNNSparseXYQAOASolver\n",
                "\n",
                "gnn_solver = GNNSparseXYQAOASolver()\n",
                "gnn_res = gnn_solver.solve(\n",
                "    cov=denoised_cov[:8, :8],\n",
                "    mu=mu[:8],\n",
                "    k_cardinality=3,\n",
                "    tickers=tickers[:8],\n",
                "    depth=1\n",
                ")\n",
                "\n",
                "print(f\"[GQML] GNN Selected Tickers: {gnn_res.selected_tickers}\")\n",
                "print(f\"[GQML] Subspace Feasibility: {gnn_res.feasibility_rate * 100.0:.1f}%\")\n",
                "print(f\"[GQML] CNOT Gate Reduction: -{gnn_res.metadata['cnot_reduction_pct']}% relative to all-to-all\")\n",
                "print(f\"[GQML] Commutation Error with Total Z: {gnn_res.metadata['commutation_error']:.2e}\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 10. Conformal Uncertainty Quantification (UQ)\n",
                "\n",
                "Computes distribution-free 95% conformal prediction bands combining empirical market ",
                "non-exchangeability with finite-shot quantum measurement multinomial noise.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from app.metrics.conformal import compute_conformal_portfolio_bounds\n",
                "\n",
                "conformal_res = compute_conformal_portfolio_bounds(\n",
                "    returns_df=prices.pct_change().dropna(),\n",
                "    weights=weights,\n",
                "    selected_indices=caf_res['selected_indices'],\n",
                "    shots=1024,\n",
                "    alpha=0.05\n",
                ")\n",
                "\n",
                "print(f\"[CONFORMAL UQ] Coverage Guarantee: {conformal_res['coverage_guarantee']}\")\n",
                "print(f\"[CONFORMAL UQ] 95% Conformal Return Interval: {conformal_res['conformal_return_interval_pct']}%\")\n",
                "print(f\"[CONFORMAL UQ] 95% Conformal Sharpe Interval: {conformal_res['conformal_sharpe_interval']}\")\n",
                "print(f\"[CONFORMAL UQ] Quantum Shot Uncertainty Margin: +/- {conformal_res['quantum_shot_noise_bps']} bps\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 11. Institutional Crisis Stress-Testing (2026 Liquidity Crunch)\n",
                "\n",
                "Simulates systemic correlation breakdown ($\\rho \\to 0.85$) to evaluate maximum drawdown ",
                "and tail risk (CVaR 95%) protection against Classical Markowitz.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from app.finance.stress_testing import run_systemic_crisis_stress_test\n",
                "\n",
                "stress_report = run_systemic_crisis_stress_test(\n",
                "    scenario='CRISIS_2026_LIQUIDITY',\n",
                "    k_cardinality=3,\n",
                "    asset_count=8,\n",
                "    transaction_cost_bps=5.0\n",
                ")\n",
                "comp = stress_report['comparison']\n",
                "\n",
                "print(f\"[STRESS TEST] Classical Markowitz Max Drawdown: {comp['classical_markowitz']['max_drawdown_pct']}%\")\n",
                "print(f\"[STRESS TEST] Q-FRONTIER (Quantum) Max Drawdown: {comp['q_frontier']['max_drawdown_pct']}%\")\n",
                "print(f\"[STRESS TEST] Drawdown Mitigation Advantage: +{comp['drawdown_mitigation_advantage_pct']}% protected\")\n",
                "print(f\"[STRESS TEST] Tail Risk (CVaR 95%) Savings: +{comp['tail_risk_cvar_savings_pct']}% saved\")\n",
                "print(f\"[STRESS TEST] QCL Adaptive Risk Setting: q = {stress_report['qcl_regime_sensor']['adapted_q_risk']} ({stress_report['qcl_regime_sensor']['risk_regime']})\")\n"
            ]
        }
    ]

    nb["cells"].extend(new_cells)
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Added Section 9, 10, and 11 to IQC_Q_FRONTIER_Master.ipynb!")
else:
    print("Section 9 already present in IQC_Q_FRONTIER_Master.ipynb.")

