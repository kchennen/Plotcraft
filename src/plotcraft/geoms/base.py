"""Base class for all geometries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import polars as pl
from matplotlib.axes import Axes

from plotcraft.core.aes import Aes


class Geom(ABC):
    """Abstract geometry — knows how to draw data onto an Axes."""

    @abstractmethod
    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw this geometry onto the given matplotlib Axes."""
        ...
