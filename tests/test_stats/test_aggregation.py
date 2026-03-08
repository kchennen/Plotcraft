"""Tests for StatCount aggregation."""

from __future__ import annotations

import polars as pl
import pytest

from plotcraft.core.aes import Aes
from plotcraft.stats.aggregation import StatCount


@pytest.fixture
def study_df() -> pl.DataFrame:
    """Small study dataset for count tests."""
    return pl.DataFrame(
        {
            "group": ["A", "A", "A", "B", "B", "C"],
            "treatment": ["ctrl", "ctrl", "drug", "ctrl", "drug", "drug"],
            "score": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        }
    )


class TestStatCount:
    """Test StatCount aggregation."""

    def test_count_by_x(self, study_df: pl.DataFrame) -> None:
        """Test counting rows grouped by x column.

        Args:
            study_df: A fixture providing a sample DataFrame for testing.

        """
        stat = StatCount()
        result = stat.compute(study_df, Aes(x="group"))
        assert "_count" in result.columns
        # A=3, B=2, C=1
        counts = dict(zip(result["group"].to_list(), result["_count"].to_list()))
        assert counts == {"A": 3, "B": 2, "C": 1}

    def test_count_by_x_and_color(self, study_df: pl.DataFrame) -> None:
        """Test counting rows grouped by x and color columns.

        Args:
            study_df: A fixture providing a sample DataFrame for testing.

        """
        stat = StatCount()
        result = stat.compute(study_df, Aes(x="group", color="treatment"))
        assert "_count" in result.columns
        assert len(result) == 5  # A-ctrl, A-drug, B-ctrl, B-drug, C-drug

    def test_count_no_grouping(self) -> None:
        """Test counting rows with no grouping (no x or color)."""
        df = pl.DataFrame({"x": [1, 2, 3]})
        stat = StatCount()
        result = stat.compute(df, Aes())
        assert result["_count"].to_list() == [3]

    def test_count_preserves_types(self, study_df: pl.DataFrame) -> None:
        """Test that count results preserve group column types.

        Args:
            study_df: A fixture providing a sample DataFrame for testing.
        """
        stat = StatCount()
        result = stat.compute(study_df, Aes(x="group"))
        assert result["group"].dtype == pl.String
        assert result["_count"].dtype.is_integer()
