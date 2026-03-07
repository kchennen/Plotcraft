"""Base class for all position adjustments."""

from __future__ import annotations

from abc import ABC, abstractmethod

import polars as pl

from plotcraft.core.aes import Aes


class Position(ABC):
    """Abstract position adjustment — offsets data to prevent overlap."""

    @abstractmethod
    def adjust(self, data: pl.DataFrame, aes: Aes, dodge_width: float) -> pl.DataFrame:
        """Adjust positions. Returns a new DataFrame."""
        ...
