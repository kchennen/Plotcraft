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
        if linewidth <= 0:
            raise ValueError(f"linewidth must be positive, got {linewidth}")
        if not (0.0 <= alpha <= 1.0):
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
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
        x_cat_map: dict[str, int] = scales.get("x_cat_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"

        if color_col and color_col in data.columns:
            for group_val in data[color_col].unique().sort().to_list():
                subset = data.filter(pl.col(color_col) == group_val)
                x_pos = self._resolve_x(subset, aes, x_cat_map)
                y_vals = subset[y_col].to_list()
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
            if aes.x:
                all_x = data[aes.x].unique().sort().to_list()
                self._apply_x_ticks(ax, all_x, x_cat_map)
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            x_pos = self._resolve_x(data, aes, x_cat_map)
            y_vals = data[y_col].to_list()
            ax.plot(
                x_pos,
                y_vals,
                linewidth=self.linewidth,
                alpha=self.alpha,
                zorder=2,
                **self.kwargs,
            )
            if aes.x:
                self._apply_x_ticks(ax, x_vals, x_cat_map)


class GeomArea(Geom):
    """Draw filled area under a line."""

    def __init__(self, alpha: float = 0.4, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize GeomArea.

        Args:
            alpha: Opacity of filled area (default 0.4).
            **kwargs: Additional keyword arguments passed to ax.fill_between().
        """
        if not (0.0 <= alpha <= 1.0):
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
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
        x_cat_map: dict[str, int] = scales.get("x_cat_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"

        if color_col and color_col in data.columns:
            for group_val in data[color_col].unique().sort().to_list():
                subset = data.filter(pl.col(color_col) == group_val)
                x_pos = self._resolve_x(subset, aes, x_cat_map)
                y_vals = subset[y_col].to_list()
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
            if aes.x:
                all_x = data[aes.x].unique().sort().to_list()
                self._apply_x_ticks(ax, all_x, x_cat_map)
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            x_pos = self._resolve_x(data, aes, x_cat_map)
            y_vals = data[y_col].to_list()
            ax.fill_between(x_pos, y_vals, alpha=self.alpha, zorder=2, **self.kwargs)
            if aes.x:
                self._apply_x_ticks(ax, x_vals, x_cat_map)
