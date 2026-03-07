"""Base class for all statistical transformations."""

from __future__ import annotations

from abc import ABC, abstractmethod

import polars as pl

from plotcraft.core.aes import Aes


class Stat(ABC):
    """Abstract stat — transforms data before drawing."""

    @abstractmethod
    def compute(self, data: pl.DataFrame, aes: Aes) -> pl.DataFrame:
        """Transform data. Returns a new DataFrame."""
        ...
