"""Base class for all position adjustments."""

from __future__ import annotations

from abc import ABC, abstractmethod

import polars as pl

from plotcraft.core.aes import Aes


class Position(ABC):
    """Abstract position adjustment — offsets data to prevent overlap."""

    @abstractmethod
    def adjust(self, data: pl.DataFrame, aes: Aes, dodge_width: float) -> pl.DataFrame:
        """Adjust positions. Returns a new DataFrame.

        Args:
            data: The input DataFrame with position columns.
            aes: The resolved aesthetic mapping.
            dodge_width: External context width supplied by the caller (e.g.
                bar width from a geometry).  Subclasses decide whether to use
                this value or their own configured width.
        """
        ...
