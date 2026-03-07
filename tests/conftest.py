"""Shared test fixtures."""

import polars as pl
import pytest


@pytest.fixture
def gene_response_df() -> pl.DataFrame:
    """A 24-row synthetic drug response study dataset."""
    return pl.DataFrame(
        {
            "gene": ["BRCA1"] * 8 + ["TP53"] * 8 + ["EGFR"] * 8,
            "expression": [
                5.2,
                4.8,
                5.5,
                5.1,
                8.3,
                7.9,
                8.7,
                8.1,
                3.1,
                3.5,
                2.9,
                3.3,
                6.4,
                6.8,
                6.1,
                6.6,
                7.0,
                7.4,
                6.8,
                7.2,
                4.5,
                4.1,
                4.8,
                4.3,
            ],
            "treatment": (["control"] * 4 + ["treated"] * 4) * 3,
            "replicate": [1, 2, 3, 4] * 6,
        }
    )


@pytest.fixture
def sample_df() -> pl.DataFrame:
    """A small DataFrame suitable for scatter, bar, and grouped plots."""
    return pl.DataFrame(
        {
            "group": ["A", "A", "A", "B", "B", "B", "C", "C", "C"],
            "value": [4.2, 3.8, 4.5, 6.1, 5.9, 6.3, 5.0, 5.2, 4.8],
            "treatment": ["ctrl", "ctrl", "ctrl", "drug", "drug", "drug", "ctrl", "ctrl", "ctrl"],
        }
    )


@pytest.fixture
def simple_df() -> pl.DataFrame:
    """Minimal 2-column DataFrame."""
    return pl.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 1, 5, 3],
        }
    )
