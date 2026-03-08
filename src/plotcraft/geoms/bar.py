"""GeomBar and GeomDash — bar chart geometries."""

from __future__ import annotations

from typing import Any

import polars as pl
from matplotlib.axes import Axes

from plotcraft.core.aes import Aes
from plotcraft.geoms.base import Geom


class GeomBar(Geom):
    """Draw vertical bars."""

    def __init__(self, width: float = 0.7, alpha: float = 0.85, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize GeomBar.

        Args:
            width: Total width of bars at each x position (default 0.7).
            alpha: Opacity of bars (default 0.85).
            **kwargs: Additional keyword arguments passed to ax.bar().
        """
        self.width = width
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
        """Draw bars grouped by color.

        Args:
            ax: Matplotlib Axes to draw on.
            data: Data frame with columns for aesthetics.
            aes: Aesthetic mappings.
            scales: Scale information (e.g. color mapping).
            theme: Theme information (not used here).

        Returns:
            None. Modifies the Axes in place.
        """
        color_map: dict[str, str] = scales.get("color_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"

        if color_col and color_col in data.columns:
            groups = data[color_col].unique().sort().to_list()
            n_groups = len(groups)
            bar_width = self.width / max(n_groups, 1)

            for i, group_val in enumerate(groups):
                subset = data.filter(pl.col(color_col) == group_val)
                x_vals = subset[aes.x].to_list() if aes.x else list(range(len(subset)))
                y_vals = subset[y_col].to_list()
                # Convert categorical x to numeric positions
                all_x = data[aes.x].unique().sort().to_list() if aes.x else x_vals
                x_pos = [all_x.index(v) + (i - (n_groups - 1) / 2) * bar_width for v in x_vals]
                color = color_map.get(str(group_val), "#333333")
                ax.bar(
                    x_pos,
                    y_vals,
                    width=bar_width,
                    alpha=self.alpha,
                    color=color,
                    label=str(group_val),
                    zorder=2,
                    **self.kwargs,
                )
            if aes.x:
                all_x = data[aes.x].unique().sort().to_list()
                ax.set_xticks(range(len(all_x)))
                ax.set_xticklabels([str(v) for v in all_x])
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            y_vals = data[y_col].to_list()
            ax.bar(
                range(len(x_vals)),
                y_vals,
                width=self.width,
                alpha=self.alpha,
                zorder=2,
                **self.kwargs,
            )
            if aes.x:
                ax.set_xticks(range(len(x_vals)))
                ax.set_xticklabels([str(v) for v in x_vals])


class GeomDash(Geom):
    """Draw horizontal dashes (hlines) at summary values."""

    def __init__(self, linewidth: float = 2.0, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize GeomDash.

        Args:
            linewidth: Width of dashes (default 2.0).
            **kwargs: Additional keyword arguments passed to ax.hlines().
        """
        self.linewidth = linewidth
        self.kwargs = kwargs

    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw horizontal line segments.

        Args:
            ax: Matplotlib Axes to draw on.
            data: Data frame with columns for aesthetics.
            aes: Aesthetic mappings.
            scales: Scale information (e.g. color mapping).
            theme: Theme information (not used here).

        Returns:
            None. Modifies the Axes in place.
        """
        color_map: dict[str, str] = scales.get("color_map", {})
        color_col = aes.color or aes.fill
        y_col = aes.y or "_count"
        dash_width = 0.3

        if color_col and color_col in data.columns:
            groups = data[color_col].unique().sort().to_list()
            n_groups = len(groups)
            all_x = data[aes.x].unique().sort().to_list() if aes.x else []

            for i, group_val in enumerate(groups):
                subset = data.filter(pl.col(color_col) == group_val)
                x_vals = subset[aes.x].to_list() if aes.x else list(range(len(subset)))
                y_vals = subset[y_col].to_list()
                color = color_map.get(str(group_val), "#333333")
                for x_val, y_val in zip(x_vals, y_vals):
                    x_pos = all_x.index(x_val) + (i - (n_groups - 1) / 2) * (0.7 / n_groups)
                    ax.hlines(
                        y_val,
                        x_pos - dash_width / 2,
                        x_pos + dash_width / 2,
                        colors=color,
                        linewidth=self.linewidth,
                        zorder=3,
                        label=str(group_val) if x_val == x_vals[0] else "_nolegend_",
                        **self.kwargs,
                    )
            if aes.x:
                ax.set_xticks(range(len(all_x)))
                ax.set_xticklabels([str(v) for v in all_x])
        else:
            x_vals = data[aes.x].to_list() if aes.x else list(range(len(data)))
            y_vals = data[y_col].to_list()
            for j, (x_val, y_val) in enumerate(zip(x_vals, y_vals)):
                ax.hlines(
                    y_val,
                    j - dash_width / 2,
                    j + dash_width / 2,
                    linewidth=self.linewidth,
                    zorder=3,
                    **self.kwargs,
                )
            if aes.x:
                ax.set_xticks(range(len(x_vals)))
                ax.set_xticklabels([str(v) for v in x_vals])
