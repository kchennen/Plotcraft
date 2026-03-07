"""PositionIdentity — no position adjustment."""

from __future__ import annotations

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.positions.base import Position


class PositionIdentity(Position):
    """No-op position. Returns data as-is."""

    def adjust(self, data: pl.DataFrame, aes: Aes, dodge_width: float) -> pl.DataFrame:
        """Return data unchanged.

        Args:
            data: The input DataFrame with position columns.
            aes: The resolved aesthetic mapping.
            dodge_width: The total width available for dodging (unused).

        Returns:
            The input DataFrame unmodified.
        """
        return data
