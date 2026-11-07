"""
Q-FRONTIER: Quantum Financial Regime-Adaptive Optimization
Context-Aware Folding (CAF) Coordinator & Monotonic Global Descent
Based on Yang, Dou, & Guo (arXiv:2609.15708, Sep 2026) and arXiv:2610.00736 (Oct 2026).
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple
import numpy as np
from app.ccd_qaoa_solver import CCDQAOASolver


class CAFCoordinator:
    """
    Context-Aware Folding (CAF) Multi-Cluster Quantum-Classical Coordinator.
    Preserves cross-cluster covariance via global context injection: v = Sigma * x.
    Guarantees monotonic global energy reduction: Delta O <= -epsilon.
    """
    def __init__(
        self,
        denoised_cov: np.ndarray,
        expected_returns: np.ndarray,
        clusters: list[dict[str, Any]],
        q_risk: float = 0.6,
        continuity_bonus: float = 0.05,
        prev_portfolio: np.ndarray | None = None
    ):
        self.cov = denoised_cov
        self.mu = expected_returns
        self.clusters = clusters
        self.n_total = len(expected_returns)
        self.q_risk = q_risk
        self.continuity_bonus = continuity_bonus
        self.prev_portfolio = prev_portfolio if prev_portfolio is not None else np.zeros(self.n_total)
        
    def evaluate_global_objective(self, x: np.ndarray) -> float:
        """Computes global scalarized energy: q * x^T Sigma x - (1-q) * mu^T x - kappa * x_prev^T x."""
        variance = float(x @ self.cov @ x)
        ret = float(np.dot(self.mu, x))
        turnover_penalty = float(self.continuity_bonus * np.dot(self.prev_portfolio, x))
        return self.q_risk * variance - (1.0 - self.q_risk) * ret - turnover_penalty

    def run_caf_coordination(
        self,
        k_per_cluster: int = 2,
        max_outer_iterations: int = 2,
        depth: int = 1
    ) -> dict[str, Any]:
        """
        Executes Context-Aware Folding outer coordination loop across all clusters.
        Returns:
            - Final global binary selection x
            - Trajectory of global energies
            - Cluster-level quantum solver diagnostics
            - Risk reduction percentage vs static decomposition
        """
        # Static baseline initialization: optimize each cluster independently with v_ext = 0
        x_static = np.zeros(self.n_total, dtype=float)
        static_cluster_details = []
        
        for c in self.clusters:
            c_idx = c["indices"]
            k_c = min(k_per_cluster, len(c_idx))
            sub_cov = self.cov[np.ix_(c_idx, c_idx)]
            sub_mu = self.mu[c_idx]
            sub_prev = self.prev_portfolio[c_idx]
            
            solver = CCDQAOASolver(n_qubits=len(c_idx), k_cardinality=k_c)
            res = solver.solve(
                cov_sub=sub_cov,
                mu_sub=sub_mu,
                q_risk=self.q_risk,
                v_ext=np.zeros(len(c_idx)),  # Static has no external context
                continuity_bonus=self.continuity_bonus,
                x_prev=sub_prev,
                depth=depth
            )
            for local_i, global_i in enumerate(c_idx):
                x_static[global_i] = res["optimal_selection"][local_i]
            static_cluster_details.append(res)
            
        static_energy = self.evaluate_global_objective(x_static)
        static_variance = float(x_static @ self.cov @ x_static)
        static_return = float(np.dot(self.mu, x_static))

        # Context-Aware Folding (CAF) Iterative Optimization
        x_caf = x_static.copy()
        v_context = self.cov @ x_caf
        energy_trajectory = [static_energy]
        caf_cluster_details = []
        
        for iteration in range(max_outer_iterations):
            for c in self.clusters:
                c_idx = c["indices"]
                k_c = min(k_per_cluster, len(c_idx))
                sub_cov = self.cov[np.ix_(c_idx, c_idx)]
                sub_mu = self.mu[c_idx]
                sub_prev = self.prev_portfolio[c_idx]
                
                # Extract external risk field: v_ext = v_C - Sigma_CC * x_C
                v_sub = v_context[c_idx]
                x_sub = x_caf[c_idx]
                v_ext = v_sub - (sub_cov @ x_sub)
                
                solver = CCDQAOASolver(n_qubits=len(c_idx), k_cardinality=k_c)
                res = solver.solve(
                    cov_sub=sub_cov,
                    mu_sub=sub_mu,
                    q_risk=self.q_risk,
                    v_ext=v_ext,
                    continuity_bonus=self.continuity_bonus,
                    x_prev=sub_prev,
                    depth=depth
                )
                
                candidate_sub = np.array(res["optimal_selection"], dtype=float)
                delta_sub = candidate_sub - x_sub
                
                if np.any(delta_sub != 0):
                    # Local monotonic acceptance check: Delta O <= -1e-6
                    delta_energy = (
                        self.q_risk * (delta_sub @ sub_cov @ delta_sub + 2.0 * np.dot(v_sub, delta_sub))
                        - (1.0 - self.q_risk) * np.dot(sub_mu, delta_sub)
                        - self.continuity_bonus * np.dot(sub_prev, delta_sub)
                    )
                    
                    if delta_energy < -1e-6:
                        # Commit update and update context vector: v <- v + Sigma[:, C] * delta_x
                        x_caf[c_idx] = candidate_sub
                        v_context += self.cov[:, c_idx] @ delta_sub
                        current_global_energy = self.evaluate_global_objective(x_caf)
                        energy_trajectory.append(current_global_energy)
                        
                if iteration == max_outer_iterations - 1:
                    caf_cluster_details.append(res)

        caf_energy = self.evaluate_global_objective(x_caf)
        caf_variance = float(x_caf @ self.cov @ x_caf)
        caf_return = float(np.dot(self.mu, x_caf))
        
        # Risk reduction metrics
        risk_reduction_pct = 0.0
        if static_variance > 1e-8:
            risk_reduction_pct = float(((static_variance - caf_variance) / static_variance) * 100.0)

        selected_indices = np.where(x_caf > 0.5)[0].tolist()

        return {
            "selected_indices": selected_indices,
            "selection_vector": x_caf.tolist(),
            "static_energy": static_energy,
            "caf_energy": caf_energy,
            "static_variance": static_variance,
            "caf_variance": caf_variance,
            "static_return": static_return,
            "caf_return": caf_return,
            "risk_reduction_pct": risk_reduction_pct,
            "energy_trajectory": energy_trajectory,
            "clusters_solved": len(self.clusters),
            "cluster_details": caf_cluster_details if caf_cluster_details else static_cluster_details
        }
