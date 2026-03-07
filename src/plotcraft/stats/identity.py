"""StatIdentity — passthrough stat that returns data unchanged."""

from __future__ import annotations

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.stats.base import Stat


class StatIdentity(Stat):
    """No-op stat. Returns data as-is."""

    def compute(self, data: pl.DataFrame, aes: Aes) -> pl.DataFrame:
        """Return data unchanged.

        Args:
            data: The input DataFrame to transform.
            aes: The resolved aesthetic mapping.

        Returns:
            The input DataFrame unmodified.
        """
        return data
