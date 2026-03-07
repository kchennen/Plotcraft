"""Dataset loader with caching."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import polars as pl

_DATA_DIR = Path(__file__).parent / "datasets"


@lru_cache(maxsize=16)
def load_dataset(name: str) -> pl.DataFrame:
    """Load a bundled dataset by name.

    Returns a Polars DataFrame. Results are cached — calling the same name
    twice returns the same DataFrame object.

    Args:
        name: Dataset name (without .csv extension). One of: energy, study,
              time_course, animals, distributions, gene_expression, climate,
              dinosaurs, eu_countries, spendings, pca.

    Returns:
        A Polars DataFrame.

    Raises:
        ValueError: If the dataset name is not recognized.
    """
    path = _DATA_DIR / f"{name}.csv"
    if not path.exists():
        available = sorted(p.stem for p in _DATA_DIR.glob("*.csv"))
        msg = f"Unknown dataset '{name}'. Available: {', '.join(available)}"
        raise ValueError(msg)
    return pl.read_csv(path)
