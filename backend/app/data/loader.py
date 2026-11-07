"""
Data loader service managing synthetic presets and custom cached CSV datasets.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd

from app.data.synthetic import generate_synthetic_prices, PRESET_UNIVERSES


class DatasetManager:
    """Manages synthetic datasets, custom uploads, and caching."""

    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            self.cache_dir = Path(__file__).resolve().parent.parent / "data_cache"
        else:
            self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._custom_datasets: Dict[str, pd.DataFrame] = {}

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
        elif dataset_id in self._custom_datasets:
            return self._custom_datasets[dataset_id]
        else:
            # Default fallback to synthetic nasdaq 12
            return generate_synthetic_prices(PRESET_UNIVERSES["NASDAQ_12"], days=days, seed=42)

    def store_custom_dataset(self, dataset_id: str, df: pd.DataFrame) -> None:
        """Stores custom validated dataset in memory and persistent cache."""
        self._custom_datasets[dataset_id] = df
        try:
            cache_file = self.cache_dir / f"{dataset_id}.csv"
            df.to_csv(cache_file)
        except Exception:
            pass


dataset_manager = DatasetManager()
