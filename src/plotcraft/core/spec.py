"""PlotSpec — the immutable plot state container."""

from __future__ import annotations

from dataclasses import dataclass, field

import polars as pl

from plotcraft.colors.discrete import colors_discrete_friendly
from plotcraft.colors.palettes import ColorScheme
from plotcraft.core.aes import Aes
from plotcraft.core.layer import Layer
from plotcraft.themes.base import THEME_PLOTCRAFT, Theme


@dataclass(frozen=True, slots=True)
class PlotSpec:
    """Complete, immutable specification of a plot.

    Every mutation creates a new instance via dataclasses.replace().
    """

    # --- Core data binding ---
    data: pl.DataFrame
    aes: Aes

    # --- Composition ---
    layers: tuple[Layer, ...] = ()

    # --- Visual style ---
    theme: Theme = field(default_factory=lambda: THEME_PLOTCRAFT)
    color_scheme: ColorScheme = field(default_factory=lambda: colors_discrete_friendly)

    # --- Dimensions (mm) ---
    width_mm: float = 50.0
    height_mm: float = 50.0

    # --- Titles & captions ---
    title: str = ""
    caption: str = ""
    x_title: str | None = None  # None = auto-derive from aes.x; "" = removed
    y_title: str | None = None  # None = auto-derive from aes.y; "" = removed

    # --- Position adjustment ---
    dodge_width: float = 0.8

    # --- Padding (top, right, bottom, left) ---
    padding: tuple[float, float, float, float] = (0.05, 0.05, 0.05, 0.05)

    # --- Color override ---
    color_map_override: dict[str, str] = field(default_factory=lambda: {})

    # --- Debug ---
    history: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate field values after construction."""
        if self.width_mm <= 0:
            raise ValueError(f"width_mm must be positive, got {self.width_mm}")
        if self.height_mm <= 0:
            raise ValueError(f"height_mm must be positive, got {self.height_mm}")
        if not (0 < self.dodge_width <= 2):
            raise ValueError(f"dodge_width must be in (0, 2], got {self.dodge_width}")
        if len(self.padding) != 4 or not all(0.0 <= p <= 1.0 for p in self.padding):
            raise ValueError(f"padding must be exactly 4 floats each in [0, 1], got {self.padding}")
