"""Dataset loader with caching."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import polars as pl

_DATA_DIR = Path(__file__).parent / "datasets"


def list_datasets() -> list[str]:
    """Return a sorted list of all available bundled dataset names.

    This is the single source of truth for which datasets exist; both
    ``load_dataset``'s docstring and the test suite derive their lists from
    here, so adding a CSV to the datasets directory is the only change needed.

    Returns:
        Sorted list of dataset name strings (without the ``.csv`` extension).
    """
    return sorted(p.stem for p in _DATA_DIR.glob("*.csv"))


@lru_cache(maxsize=16)
def load_dataset(name: str) -> pl.DataFrame:
    """Load a bundled dataset by name.

    Returns a Polars DataFrame. Results are cached — calling the same name
    twice returns the same DataFrame object.

    Use ``list_datasets()`` to programmatically discover all available names.

    Args:
        name: Dataset name (without .csv extension).
              Run ``pc.list_datasets()`` for the full list.

    Returns:
        A Polars DataFrame.

    Raises:
        ValueError: If the dataset name is not recognized.
    """
    path = _DATA_DIR / f"{name}.csv"
    if not path.exists():
        available = list_datasets()
        msg = f"Unknown dataset '{name}'. Available: {', '.join(available)}"
        raise ValueError(msg)
    return pl.read_csv(path)
