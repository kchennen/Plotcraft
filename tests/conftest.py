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
