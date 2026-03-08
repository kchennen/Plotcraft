"""Aggregation stats — StatCount (and later StatMean, StatMedian, StatSum)."""

from __future__ import annotations

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.stats.base import Stat


class StatCount(Stat):
    """Count rows per group.

    Groups by the x column (and color column if present), producing
    a _count column used by count geometries as the y aesthetic.
    """

    def compute(self, data: pl.DataFrame, aes: Aes) -> pl.DataFrame:
        """Compute row counts per group.

        Args:
            data: Input data frame.
            aes: Aesthetic mappings.

        Returns:
            Data frame with group columns and a _count column.
        """
        group_cols: list[str] = []
        if aes.x and aes.x in data.columns:
            group_cols.append(aes.x)
        color_col = aes.color or aes.fill
        if color_col and color_col in data.columns and color_col not in group_cols:
            group_cols.append(color_col)

        if not group_cols:
            # No grouping — count all rows
            return pl.DataFrame({"_count": [len(data)]})

        return data.group_by(group_cols).agg(pl.len().alias("_count")).sort(group_cols)
