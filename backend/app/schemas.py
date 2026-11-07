"""
Pydantic schemas and data transfer objects for Q-FRONTIER REST API.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    dataset_id: str = Field("synthetic_nasdaq_8", description="ID of dataset to load.")
    asset_count: int = Field(8, ge=4, le=12, description="Number of assets N (qubit count).")
    k_cardinality: int = Field(3, ge=1, le=11, description="Exact number of assets to select K.")
    lambda_risk: float = Field(0.5, ge=0.0, le=1.0, description="Risk aversion parameter lambda in [0, 1].")
    covariance_method: str = Field("ledoit_wolf", description="'ledoit_wolf', 'sample', or 'rmt'.")
    solvers: List[str] = Field(
        default_factory=lambda: ["exact", "annealing", "xy_qaoa", "ccd_qaoa", "penalty_qaoa"],
        description="Solvers to benchmark."
    )
    circuit_depth: int = Field(1, ge=1, le=2, description="QAOA circuit depth p (1 or 2).")
    seeds: List[int] = Field(
        default_factory=lambda: [42, 101, 777],
        description="Random seeds for heuristic and statistical spread."
    )
    transaction_cost_bps: float = Field(5.0, ge=0.0, le=50.0, description="Transaction fee in basis points.")
    turnover_penalty: float = Field(0.05, ge=0.0, le=0.5, description="Turnover continuity bonus.")


class CSVValidateRequest(BaseModel):
    csv_content: str = Field(..., description="Raw CSV string with date and price columns.")
    dataset_id: Optional[str] = Field(None, description="Optional unique identifier to save the dataset under.")


class OptimizationRequest(BaseModel):
    """Legacy request schema retained for backward compatibility."""
    q_risk: Optional[float] = Field(None, ge=0.0, le=1.0, description="Risk aversion constant.")
    continuity_bonus: float = Field(0.05, ge=0.0, le=0.5, description="Continuity bonus kappa.")
    depth: int = Field(1, ge=1, le=2, description="Circuit depth p.")
    use_qcl_sensor: bool = Field(True, description="Whether to tune risk aversion via QCL.")
    transaction_cost_bps: float = Field(5.0, ge=0.0, le=50.0, description="Transaction fee in basis points.")
