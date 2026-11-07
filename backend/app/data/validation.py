"""
Data validation utilities for user-uploaded CSV price series.
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple
import io
import pandas as pd
import numpy as np


def validate_price_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates a pandas DataFrame containing asset prices.
    Rules:
      - Must contain at least 2 assets and 10 rows.
      - Date index or Date column parseable as dates.
      - All asset prices must be strictly positive numeric values.
      - No all-NaN columns.
      - Flags missing values and reports clean diagnostics.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # If Date is a column, set as index
    date_cols = [c for c in df.columns if "date" in str(c).lower() or "time" in str(c).lower()]
    if date_cols and not isinstance(df.index, pd.DatetimeIndex):
        try:
            df = df.set_index(pd.to_datetime(df[date_cols[0]]))
            df = df.drop(columns=[date_cols[0]])
        except Exception as e:
            errors.append(f"Could not parse date column '{date_cols[0]}': {e}")

    # Keep only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    asset_cols = list(numeric_df.columns)

    non_date_cols = [c for c in df.columns if c not in date_cols]
    dropped_cols = [c for c in non_date_cols if c not in asset_cols]
    if dropped_cols:
        warnings.append(f"Excluded non-numeric column(s): {dropped_cols}")

    if len(asset_cols) < 2:
        errors.append(f"Dataset must contain at least 2 numeric asset price columns. Found: {len(asset_cols)}")

    if len(df) < 10:
        errors.append(f"Dataset must contain at least 10 observations. Found: {len(df)}")

    # Check for non-positive values
    non_positive_counts = (numeric_df <= 0).sum().to_dict()
    bad_assets = [k for k, v in non_positive_counts.items() if v > 0]
    if bad_assets:
        errors.append(f"Asset prices must be strictly positive. Found non-positive values in: {bad_assets}")

    # Missing value audit
    null_counts = numeric_df.isnull().sum().to_dict()
    total_nulls = int(sum(null_counts.values()))
    if total_nulls > 0:
        warnings.append(f"Dataset contains {total_nulls} missing values across {len([k for k, v in null_counts.items() if v > 0])} assets. Forward-fill will be applied.")

    start_date = str(df.index[0]) if len(df) > 0 else None
    end_date = str(df.index[-1]) if len(df) > 0 else None

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "num_assets": len(asset_cols),
        "num_observations": len(df),
        "assets": asset_cols,
        "start_date": start_date,
        "end_date": end_date,
        "missing_values_count": total_nulls,
    }


def parse_and_validate_csv(csv_content: str | bytes) -> Tuple[bool, Dict[str, Any], Optional[pd.DataFrame]]:
    """
    Parses raw CSV string or bytes, validates it, and returns clean DataFrame.
    """
    try:
        if isinstance(csv_content, bytes):
            buffer = io.BytesIO(csv_content)
        else:
            buffer = io.StringIO(csv_content)

        df = pd.read_csv(buffer)
        diag = validate_price_dataframe(df)

        if not diag["is_valid"]:
            return False, diag, None

        # Clean dataframe
        date_cols = [c for c in df.columns if "date" in str(c).lower() or "time" in str(c).lower()]
        if date_cols and not isinstance(df.index, pd.DatetimeIndex):
            df = df.set_index(pd.to_datetime(df[date_cols[0]]))
            df = df.drop(columns=[date_cols[0]])

        clean_df = df.select_dtypes(include=[np.number]).ffill().bfill()
        return True, diag, clean_df
    except Exception as e:
        return False, {
            "is_valid": False,
            "errors": [f"CSV parsing error: {str(e)}"],
            "warnings": [],
            "num_assets": 0,
            "num_observations": 0,
            "assets": [],
            "start_date": None,
            "end_date": None,
            "missing_values_count": 0,
        }, None
