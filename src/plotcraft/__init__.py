"""Plotcraft — Crafting publication-ready statistical graphics in Python."""

from __future__ import annotations

from typing import Any

from plotcraft._compat import ensure_polars
from plotcraft._version import __version__
from plotcraft.colors import (
    # Continuous
    colors_continuous_bluepinkyellow,
    colors_continuous_cividis,
    colors_continuous_inferno,
    colors_continuous_magma,
    colors_continuous_mako,
    colors_continuous_plasma,
    colors_continuous_rocket,
    colors_continuous_turbo,
    colors_continuous_viridis,
    # Discrete
    colors_discrete_alger,
    colors_discrete_apple,
    colors_discrete_candy,
    colors_discrete_friendly_long,
    colors_discrete_ibm,
    colors_discrete_metro,
    colors_discrete_okabeito,
    colors_discrete_rainbow,
    colors_discrete_seaside,
    colors_discrete_tableau10,
    colors_discrete_tol_light,
    colors_discrete_tol_muted,
    colors_discrete_tol_vibrant,
    colors_discrete_wong,
    # Diverging
    colors_diverging_blue2brown,
    colors_diverging_blue2red,
    colors_diverging_BuRd,
    colors_diverging_BuYlRd,
    colors_diverging_icefire,
    colors_diverging_spectral,
    # Journal
    colors_journal_aaas,
    colors_journal_d3,
    colors_journal_igv,
    colors_journal_jama,
    colors_journal_lancet,
    colors_journal_nejm,
    colors_journal_npg,
    new_color_scheme,
)
from plotcraft.colors.palettes import ColorScheme
from plotcraft.core.aes import Aes
from plotcraft.core.options import get_options
from plotcraft.core.plot import PlotCraft
from plotcraft.core.spec import PlotSpec
from plotcraft.data import load_dataset
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
    # Continuous
    "colors_continuous_bluepinkyellow",
    "colors_continuous_cividis",
    "colors_continuous_inferno",
    "colors_continuous_magma",
    "colors_continuous_mako",
    "colors_continuous_plasma",
    "colors_continuous_rocket",
    "colors_continuous_turbo",
    "colors_continuous_viridis",
    # Discrete
    "colors_discrete_alger",
    "colors_discrete_apple",
    "colors_discrete_candy",
    "colors_discrete_friendly_long",
    "colors_discrete_ibm",
    "colors_discrete_metro",
    "colors_discrete_okabeito",
    "colors_discrete_rainbow",
    "colors_discrete_seaside",
    "colors_discrete_tableau10",
    "colors_discrete_tol_light",
    "colors_discrete_tol_muted",
    "colors_discrete_tol_vibrant",
    "colors_discrete_wong",
    "colors_diverging_BuRd",
    "colors_diverging_BuYlRd",
    # Diverging
    "colors_diverging_blue2brown",
    "colors_diverging_blue2red",
    "colors_diverging_icefire",
    "colors_diverging_spectral",
    # Journal
    "colors_journal_aaas",
    "colors_journal_d3",
    "colors_journal_igv",
    "colors_journal_jama",
    "colors_journal_lancet",
    "colors_journal_nejm",
    "colors_journal_npg",
    "ensure_polars",
    "load_dataset",
    "new_color_scheme",
    "plotcraft",
]
