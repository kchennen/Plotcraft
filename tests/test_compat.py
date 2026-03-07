"""Tests for Polars/pandas compatibility."""

import polars as pl
import pytest

from plotcraft._compat import ensure_polars


def test_polars_passthrough():
    df = pl.DataFrame({"a": [1, 2]})
    result = ensure_polars(df)
    assert result is df


def test_rejects_non_dataframe():
    with pytest.raises(TypeError, match="Expected Polars or pandas"):
        ensure_polars({"a": [1, 2]})


def test_pandas_conversion():
    pytest.importorskip("pandas")
    import pandas as pd  # pyright: ignore[reportMissingModuleSource]

    pdf = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = ensure_polars(pdf)
    assert isinstance(result, pl.DataFrame)
    assert result.shape == (2, 2)
