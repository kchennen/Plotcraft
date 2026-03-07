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

        Uses ``self.width`` (set at construction) for the total dodge span,
        so all groups share the same configured width regardless of the
        ``dodge_width`` context supplied by the caller.

        Null values in the grouping column receive a zero offset (no dodge).

        Args:
            data: The input DataFrame with a ``_x_numeric`` position column.
            aes: The resolved aesthetic mapping (must have color or fill set).
            dodge_width: External context width from the caller (unused here;
                ``self.width`` controls the effective dodge span).

        Returns:
            A new DataFrame with ``_x_numeric`` shifted per group.
        """
        color_col = aes.color or aes.fill
        if color_col is None or aes.x is None:
            return data
        if "_x_numeric" not in data.columns:
            return data

        # Drop nulls when building groups so null rows get the zero-offset default.
        groups = data[color_col].drop_nulls().unique().sort().to_list()
        n_groups = len(groups)
        if n_groups <= 1:
            return data

        offsets = {g: (i - (n_groups - 1) / 2) * (self.width / n_groups) for i, g in enumerate(groups)}

        # Non-strict replace: unexpected / null values map to 0.0 (no offset).
        return data.with_columns(
            (pl.col("_x_numeric") + pl.col(color_col).replace(offsets, default=0.0)).alias("_x_numeric"),
        )
