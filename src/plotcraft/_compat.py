"""Polars/pandas compatibility bridge."""

from __future__ import annotations

from typing import Any

import polars as pl


def ensure_polars(data: Any) -> pl.DataFrame:  # noqa: ANN401
    """Convert input to a Polars DataFrame.

    Accepts Polars DataFrames (passthrough) or pandas DataFrames (converted).

    Args:
        data: A Polars or pandas DataFrame.

    Returns:
        A Polars DataFrame.

    Raises:
        TypeError: If input is neither Polars nor pandas.
    """
    if isinstance(data, pl.DataFrame):
        return data
    try:
        import pandas as pd

        if isinstance(data, pd.DataFrame):
            return pl.from_pandas(data)
    except ImportError:
        pass
    raise TypeError(
        f"Expected Polars or pandas DataFrame, got {type(data).__name__}. "
        "Install pandas with: pip install plotcraft[pandas]"
    )
