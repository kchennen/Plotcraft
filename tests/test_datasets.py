"""Tests for bundled datasets and the load_dataset function."""

from __future__ import annotations

import polars as pl
import pytest

from plotcraft.data.loader import list_datasets, load_dataset

# Derived from list_datasets() — adding a CSV to datasets/ is reflected
# here automatically without any manual list to maintain.
EXPECTED_DATASETS = list_datasets()


class TestLoadDataset:
    """Test dataset loading mechanics."""

    @pytest.mark.parametrize("name", EXPECTED_DATASETS)
    def test_loads_successfully(self, name: str) -> None:
        """Each dataset loads without error."""
        df = load_dataset(name)
        assert isinstance(df, pl.DataFrame)
        assert len(df) > 0

    @pytest.mark.parametrize("name", EXPECTED_DATASETS)
    def test_has_columns(self, name: str) -> None:
        """Each dataset has at least 2 columns."""
        df = load_dataset(name)
        assert len(df.columns) >= 2

    def test_unknown_dataset_raises(self) -> None:
        """Requesting a nonexistent dataset gives a helpful error."""
        with pytest.raises(ValueError, match="Unknown dataset 'nonexistent'"):
            load_dataset("nonexistent")

    def test_error_lists_available(self) -> None:
        """The error message lists available datasets."""
        with pytest.raises(ValueError, match="study"):
            load_dataset("nonexistent")

    def test_caching(self) -> None:
        """The same call twice returns the same object (lru_cache)."""
        # Clear cache first to get a clean test
        load_dataset.cache_clear()
        df1 = load_dataset("study")
        df2 = load_dataset("study")
        assert df1 is df2


class TestStudyDataset:
    """Verify the study dataset schema — it's used in the Definition of Done."""

    def test_schema(self) -> None:
        """Test that the study dataset has the expected columns."""
        df = load_dataset("study")
        assert "group" in df.columns
        assert "treatment" in df.columns
        assert "score" in df.columns
        assert "dose" in df.columns

    def test_row_count(self) -> None:
        """Test that the study dataset has the expected number of rows."""
        df = load_dataset("study")
        assert len(df) == 30  # 3 groups x 2 treatments x 5 replicates


class TestGeneExpressionDataset:
    """Verify the gene_expression dataset — used alongside gene_response."""

    def test_schema(self) -> None:
        """Test that the gene_expression dataset has the expected columns."""
        df = load_dataset("gene_expression")
        assert "gene" in df.columns
        assert "log2fc" in df.columns
        assert "pvalue" in df.columns

    def test_has_significant_column(self) -> None:
        """Test that the gene_expression dataset has a 'significant' column."""
        df = load_dataset("gene_expression")
        assert "significant" in df.columns
        values = df["significant"].unique().sort().to_list()
        assert set(values) == {"yes", "no"}
