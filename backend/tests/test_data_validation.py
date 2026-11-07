"""
Unit tests for data validation, parsing, and synthetic dataset loading.
"""

import pytest
import pandas as pd
import numpy as np

from app.data.synthetic import generate_synthetic_prices, PRESET_UNIVERSES
from app.data.validation import validate_price_dataframe, parse_and_validate_csv
from app.data.loader import DatasetManager


def test_synthetic_presets_deterministic():
    """Verify that synthetic generation is deterministic with fixed seed."""
    df1 = generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_8"], days=60, seed=42)
    df2 = generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_8"], days=60, seed=42)
    assert np.allclose(df1.values, df2.values)
    assert list(df1.columns) == PRESET_UNIVERSES["NASDAQ_8"]
    assert len(df1) == 60


def test_valid_csv_validation():
    """Verify clean CSV validation passes."""
    csv_str = (
        "Date,AAPL,MSFT,NVDA\n"
        "2026-01-01,150.0,300.0,400.0\n"
        "2026-01-02,152.0,302.0,405.0\n"
        "2026-01-03,151.0,301.0,403.0\n"
        "2026-01-04,153.0,305.0,410.0\n"
        "2026-01-05,154.0,304.0,412.0\n"
        "2026-01-06,155.0,306.0,415.0\n"
        "2026-01-07,156.0,307.0,418.0\n"
        "2026-01-08,157.0,309.0,420.0\n"
        "2026-01-09,158.0,310.0,422.0\n"
        "2026-01-10,159.0,312.0,425.0\n"
    )
    is_valid, diag, clean_df = parse_and_validate_csv(csv_str)
    assert is_valid is True
    assert diag["num_assets"] == 3
    assert diag["num_observations"] == 10
    assert clean_df is not None
    assert len(clean_df) == 10


def test_invalid_csv_negative_prices():
    """Verify non-positive prices are flagged."""
    csv_str = (
        "Date,AAPL,MSFT\n"
        "2026-01-01,-150.0,300.0\n"
        "2026-01-02,152.0,302.0\n"
    )
    is_valid, diag, clean_df = parse_and_validate_csv(csv_str)
    assert is_valid is False
    assert len(diag["errors"]) > 0
    assert clean_df is None


def test_dataset_manager_listing_and_custom_storage(tmp_path):
    """Verify dataset manager lists presets and stores custom datasets."""
    mgr = DatasetManager(cache_dir=tmp_path)
    datasets = mgr.list_datasets()
    assert len(datasets) >= 3

    custom_df = pd.DataFrame({
        "ASSET1": [10.0, 11.0, 12.0],
        "ASSET2": [20.0, 21.0, 22.0]
    })
    mgr.store_custom_dataset("custom_test_1", custom_df)
    retrieved = mgr.get_dataset("custom_test_1")
    assert retrieved.shape == (3, 2)
