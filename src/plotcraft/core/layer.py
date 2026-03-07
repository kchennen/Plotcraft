"""Layer dataclass — the composition unit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.geoms.base import Geom
from plotcraft.positions.base import Position
from plotcraft.stats.base import Stat


@dataclass(frozen=True, slots=True)
class Layer:
    """A single visual layer: geometry + stat + position + optional overrides."""

    geom: Geom
    stat: Stat
    position: Position
    aes_override: Aes = field(default_factory=Aes)
    data: pl.DataFrame | None = None
    params: dict[str, Any] = field(default_factory=lambda: {})

    def resolve_aes(self, plot_aes: Aes) -> Aes:
        """Merge plot-level aesthetics with layer overrides, then resolve fill."""
        return plot_aes.merge(self.aes_override).resolve_fill()

    def compute(self, df: pl.DataFrame, aes: Aes) -> pl.DataFrame:
        """Run the stat transformation on the data."""
        return self.stat.compute(df, aes)
