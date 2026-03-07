"""Plotcraft — Crafting publication-ready statistical graphics in Python."""

from __future__ import annotations

from typing import Any

from plotcraft._compat import ensure_polars
from plotcraft._version import __version__
from plotcraft.colors.palettes import ColorScheme, colors_discrete_friendly
from plotcraft.core.aes import Aes
from plotcraft.core.options import get_options
from plotcraft.core.plot import PlotCraft
from plotcraft.core.spec import PlotSpec
from plotcraft.themes.base import THEME_PLOTCRAFT, Theme


def plotcraft(
    data: Any,  # noqa: ANN401 — accepts pl.DataFrame or pd.DataFrame
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    *,
    fill: str | None = None,
    size: str | None = None,
    shape: str | None = None,
    alpha: str | None = None,
    group: str | None = None,
    label: str | None = None,
    width: float | None = None,
    height: float | None = None,
) -> PlotCraft:
    """Create a new plot from data and aesthetic mappings.

    This is the entry point for every Plotcraft visualization.

    Args:
        data: A Polars or pandas DataFrame.
        x: Column name for the x-axis.
        y: Column name for the y-axis.
        color: Column name for color grouping.
        fill: Column name for fill color (defaults to color).
        size: Column name for size mapping.
        shape: Column name for marker shape.
        alpha: Column name for transparency.
        group: Column name for explicit grouping.
        label: Column name for text labels.
        width: Figure width in mm (default: from global options).
        height: Figure height in mm (default: from global options).

    Returns:
        A new PlotCraft instance ready for method chaining.
    """
    df = ensure_polars(data)
    opts = get_options()

    spec = PlotSpec(
        data=df,
        aes=Aes(
            x=x,
            y=y,
            color=color,
            fill=fill,
            size=size,
            shape=shape,
            alpha=alpha,
            group=group,
            label=label,
        ),
        theme=opts.theme,
        color_scheme=opts.color_scheme,
        width_mm=width if width is not None else opts.width,
        height_mm=height if height is not None else opts.height,
    )
    return PlotCraft(spec)


__all__ = [
    "THEME_PLOTCRAFT",
    "Aes",
    "ColorScheme",
    "PlotCraft",
    "PlotSpec",
    "Theme",
    "__version__",
    "colors_discrete_friendly",
    "ensure_polars",
    "plotcraft",
]
