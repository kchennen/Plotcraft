"""GeomLine and GeomArea — line and filled area geometries."""

from __future__ import annotations

from typing import Any

import polars as pl
from matplotlib.axes import Axes

from plotcraft.core.aes import Aes
from plotcraft.geoms.base import Geom


class GeomLine(Geom):
    """Draw connected lines."""

    def __init__(self, linewidth: float = 1.5, alpha: float = 1.0, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize GeomLine.

        Args:
            linewidth: Width of lines (default 1.5).
            alpha: Opacity of lines (default 1.0).
            **kwargs: Additional keyword arguments passed to ax.plot().
        """
        self.linewidth = linewidth
        self.alpha = alpha
        self.kwargs = kwargs

    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw lines grouped by color.

        Args:
            ax: Matplotlib Axes to draw on.
            data: Data frame containing the data to plot.
            aes: Aesthetic mappings (e.g. x, y, color).
            scales: Dictionary of scales (e.g. color_map).
            theme: Theme settings (not used here).

        Returns:
            None. Modifies the Axes in place.
        """
        color_map: dict[str, str] = scales.get("color_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"

        if color_col and color_col in data.columns:
            all_x = data[aes.x].unique().sort().to_list() if aes.x else []
            for group_val in data[color_col].unique().sort().to_list():
                subset = data.filter(pl.col(color_col) == group_val)
                x_vals = subset[aes.x].to_list() if aes.x else list(range(len(subset)))
                y_vals = subset[y_col].to_list()
                x_pos = [all_x.index(v) for v in x_vals] if aes.x and all_x else x_vals
                color = color_map.get(str(group_val), "#333333")
                ax.plot(
                    x_pos,
                    y_vals,
                    color=color,
                    linewidth=self.linewidth,
                    alpha=self.alpha,
                    label=str(group_val),
                    zorder=2,
                    **self.kwargs,
                )
            if aes.x and all_x:
                ax.set_xticks(range(len(all_x)))
                ax.set_xticklabels([str(v) for v in all_x])
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            y_vals = data[y_col].to_list()
            x_pos = list(range(len(x_vals)))
            ax.plot(
                x_pos,
                y_vals,
                linewidth=self.linewidth,
                alpha=self.alpha,
                zorder=2,
                **self.kwargs,
            )
            if aes.x:
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(v) for v in x_vals])


class GeomArea(Geom):
    """Draw filled area under a line."""

    def __init__(self, alpha: float = 0.4, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize GeomArea.

        Args:
            alpha: Opacity of filled area (default 0.4).
            **kwargs: Additional keyword arguments passed to ax.fill_between().
        """
        self.alpha = alpha
        self.kwargs = kwargs

    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw filled areas grouped by color.

        Args:
            ax: Matplotlib Axes to draw on.
            data: Data frame containing the data to plot.
            aes: Aesthetic mappings (e.g. x, y, color).
            scales: Dictionary of scales (e.g. color_map).
            theme: Theme settings (not used here).

        Returns:
            None. Modifies the Axes in place.
        """
        color_map: dict[str, str] = scales.get("color_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"

        if color_col and color_col in data.columns:
            all_x = data[aes.x].unique().sort().to_list() if aes.x else []
            for group_val in data[color_col].unique().sort().to_list():
                subset = data.filter(pl.col(color_col) == group_val)
                x_vals = subset[aes.x].to_list() if aes.x else list(range(len(subset)))
                y_vals = subset[y_col].to_list()
                x_pos = [all_x.index(v) for v in x_vals] if aes.x and all_x else x_vals
                color = color_map.get(str(group_val), "#333333")
                ax.fill_between(
                    x_pos,
                    y_vals,
                    alpha=self.alpha,
                    color=color,
                    label=str(group_val),
                    zorder=2,
                    **self.kwargs,
                )
            if aes.x and all_x:
                ax.set_xticks(range(len(all_x)))
                ax.set_xticklabels([str(v) for v in all_x])
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            y_vals = data[y_col].to_list()
            x_pos = list(range(len(x_vals)))
            ax.fill_between(x_pos, y_vals, alpha=self.alpha, zorder=2, **self.kwargs)
            if aes.x:
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(v) for v in x_vals])
