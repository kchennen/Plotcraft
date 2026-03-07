"""PositionDodge — offset groups horizontally to prevent overlap."""

from __future__ import annotations

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.positions.base import Position


class PositionDodge(Position):
    """Offset groups horizontally so bars/points don't overlap."""

    def __init__(self, width: float = 0.8) -> None:
        """Initialize with dodge width (default 0.8).

        Args:
            width: The total dodge width shared across groups.
        """
        self.width = width

    def adjust(self, data: pl.DataFrame, aes: Aes, dodge_width: float) -> pl.DataFrame:
        """Apply horizontal dodge based on color/fill grouping.

        Args:
            data: The input DataFrame with position columns.
            aes: The resolved aesthetic mapping.
            dodge_width: The total width available for dodging.

        Returns:
            A new DataFrame with adjusted x positions.
        """
        color_col = aes.color or aes.fill
        if color_col is None or aes.x is None:
            return data
        if "_x_numeric" not in data.columns:
            return data

        groups = data[color_col].unique().sort().to_list()
        n_groups = len(groups)
        if n_groups <= 1:
            return data

        offsets = {g: (i - (n_groups - 1) / 2) * (dodge_width / n_groups) for i, g in enumerate(groups)}

        return data.with_columns((pl.col("_x_numeric") + pl.col(color_col).replace_strict(offsets)).alias("_x_numeric"))
