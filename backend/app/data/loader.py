"""
Data loader service managing synthetic presets and custom cached CSV datasets.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from collections import OrderedDict
from pathlib import Path
import re
import os
import time
import pandas as pd

from app.data.synthetic import generate_synthetic_prices, generate_crisis_prices, PRESET_UNIVERSES


class DatasetManager:
    """Manages synthetic datasets, custom uploads, and caching."""

    def __init__(self, cache_dir: Optional[Path] = None, max_custom_datasets: int = 25):
        if cache_dir is None:
            self.cache_dir = Path(__file__).resolve().parent.parent / "data_cache"
        else:
            self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._custom_datasets: OrderedDict[str, pd.DataFrame] = OrderedDict()
        self.max_custom_datasets = max_custom_datasets

    def list_datasets(self) -> List[Dict[str, Any]]:
        """Lists all available datasets (presets + custom uploads)."""
        items = [
            {
                "id": "synthetic_nasdaq_12",
                "name": "Synthetic Nasdaq-12 (Reproducible Demo)",
                "type": "synthetic",
                "assets": PRESET_UNIVERSES["NASDAQ_12"],
                "asset_count": len(PRESET_UNIVERSES["NASDAQ_12"]),
                "observations": 180,
                "description": "Standard 12-asset universe under a 3-factor market model. Seeded for reproducible offline execution.",
            },
            {
                "id": "synthetic_nasdaq_8",
                "name": "Synthetic Nasdaq-8 (Balanced Subspace)",
                "type": "synthetic",
                "assets": PRESET_UNIVERSES["NASDAQ_8"],
                "asset_count": len(PRESET_UNIVERSES["NASDAQ_8"]),
                "observations": 180,
                "description": "8-asset mega-cap tech universe. Fits exact enumeration and 8-qubit quantum simulation.",
            },
            {
                "id": "synthetic_tech_4",
                "name": "Synthetic Tech-4 (Fast Simulation)",
                "type": "synthetic",
                "assets": PRESET_UNIVERSES["TECH_4"],
                "asset_count": len(PRESET_UNIVERSES["TECH_4"]),
                "observations": 180,
                "description": "4-asset subuniverse for near-instant quantum circuit evaluation and statevector verification.",
            },
            {
                "id": "synthetic_crisis_2026",
                "name": "🚨 2026 Liquidity Crisis Shock (Stress Scenario)",
                "type": "stress_scenario",
                "assets": PRESET_UNIVERSES["CRISIS_2026"],
                "asset_count": len(PRESET_UNIVERSES["CRISIS_2026"]),
                "observations": 180,
                "description": "High-stress regime with systemic correlation breakdown (rho -> 0.85) and rough-volatility spikes.",
            },
            {
                "id": "synthetic_flash_crash",
                "name": "⚡ Flash Crash & Sector Dispersion (Stress Scenario)",
                "type": "stress_scenario",
                "assets": PRESET_UNIVERSES["FLASH_CRASH_8"],
                "asset_count": len(PRESET_UNIVERSES["FLASH_CRASH_8"]),
                "observations": 180,
                "description": "Acute liquidity vacuum shock testing instantaneous QCL risk detection and CCD-QAOA drawdown limits.",
            },
        ]

        for custom_id, df in self._custom_datasets.items():
            items.append({
                "id": custom_id,
                "name": f"Uploaded Dataset ({custom_id})",
                "type": "custom",
                "assets": list(df.columns),
                "asset_count": len(df.columns),
                "observations": len(df),
                "description": f"Custom user dataset with {len(df.columns)} assets and {len(df)} timestamps.",
            })

        return items

    def get_dataset(self, dataset_id: str, days: int = 180) -> pd.DataFrame:
        """Retrieves price DataFrame for a given dataset ID."""
        if dataset_id == "synthetic_nasdaq_12":
            return generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_12"], days=days, seed=42)
        elif dataset_id == "synthetic_nasdaq_8":
            return generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_8"], days=days, seed=42)
        elif dataset_id == "synthetic_tech_4":
            return generate_synthetic_prices(PRESET_UNIVERSES["TECH_4"], days=days, seed=42)
        elif dataset_id == "synthetic_crisis_2026":
            return generate_crisis_prices("CRISIS_2026_LIQUIDITY", tickers=PRESET_UNIVERSES["CRISIS_2026"], days=days, seed=42)
        elif dataset_id == "synthetic_flash_crash":
            return generate_crisis_prices("CRISIS_FLASH_CRASH", tickers=PRESET_UNIVERSES["FLASH_CRASH_8"], days=days, seed=42)
        elif dataset_id in self._custom_datasets:
            return self._custom_datasets[dataset_id]
        else:
            # Default fallback to synthetic nasdaq 12
            return generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_12"], days=days, seed=42)

    def store_custom_dataset(self, dataset_id: str, df: pd.DataFrame) -> str:
        """Stores custom validated dataset in memory and persistent cache securely."""
        clean_id = re.sub(r"[^a-zA-Z0-9_-]", "", dataset_id)
        if not clean_id:
            clean_id = f"custom_{int(time.time())}"
        self._custom_datasets[clean_id] = df
        self._custom_datasets.move_to_end(clean_id)

        # Evict oldest in memory if exceeding limit
        if len(self._custom_datasets) > self.max_custom_datasets:
            self._custom_datasets.popitem(last=False)

        try:
            cache_file = (self.cache_dir / f"{clean_id}.csv").resolve()
            if cache_file.is_relative_to(self.cache_dir.resolve()):
                df.to_csv(cache_file)

            # Bound disk cache to 30 files max
            csv_files = sorted(self.cache_dir.glob("custom_*.csv"), key=os.path.getmtime)
            if len(csv_files) > 30:
                for old_csv in csv_files[:-30]:
                    try:
                        old_csv.unlink()
                    except Exception:
                        pass
        except Exception:
            pass
        return clean_id


dataset_manager = DatasetManager()
