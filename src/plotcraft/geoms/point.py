"""GeomPoint — scatter plot geometry."""

from __future__ import annotations

from typing import Any

import polars as pl
from matplotlib.axes import Axes

from plotcraft.core.aes import Aes
from plotcraft.geoms.base import Geom


class GeomPoint(Geom):
    """Draw data as scatter points."""

    def __init__(
        self,
        size: float = 2.0,
        alpha: float = 1.0,
        marker: str = "o",
        show_colorbar: bool = True,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize with point size, alpha, marker style, and additional kwargs.

        Args:
            size: Point size in display points.  Passed to ``ax.scatter``
                as ``s=size²`` (marker area in points²), so the visual
                radius scales linearly with this value.
            alpha: Opacity from 0.0 (transparent) to 1.0 (opaque).
            marker: Matplotlib marker style string.
            show_colorbar: Whether to show a colorbar when using a continuous
                color scale (default True).
            **kwargs: Extra keyword arguments forwarded to ``ax.scatter``.
        """
        if size <= 0:
            raise ValueError(f"size must be positive, got {size}")
        if not (0.0 <= alpha <= 1.0):
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
        self.size = size
        self.alpha = alpha
        self.marker = marker
        self.show_colorbar = show_colorbar
        self.kwargs = kwargs

    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw scatter points, grouped by color if a color aesthetic is set.

        Args:
            ax: The matplotlib Axes to draw on.
            data: The data to visualize.
            aes: The resolved aesthetic mapping.
            scales: A dict of precomputed scale information (e.g. color_map).
            theme: The active theme controlling visual style.
        """
        color_map: dict[str, str] = scales.get("color_map", {})
        x_cat_map: dict[str, int] = scales.get("x_cat_map", {})
        color_col = aes.color or aes.fill

        # ── Continuous color path ─────────────────────────────────────────────
        if scales.get("continuous"):
            cmap = scales["colormap"]
            norm = scales["norm"]
            x_values = self._resolve_x(data, aes, x_cat_map)
            y_values = data[aes.y].to_list() if aes.y else list(range(len(data)))
            c_values = data[color_col].to_numpy() if color_col and color_col in data.columns else None
            scatter = ax.scatter(
                x_values,
                y_values,
                s=self.size**2,
                c=c_values,
                cmap=cmap,
                norm=norm,
                alpha=self.alpha,
                marker=self.marker,
                zorder=3,
                **self.kwargs,
            )
            if self.show_colorbar:
                ax.figure.colorbar(scatter, ax=ax, shrink=0.8)
            return

        # ── Discrete color path ───────────────────────────────────────────────
        if color_col and color_col in data.columns:
            for group_val in data[color_col].unique().sort().to_list():
                subset = data.filter(pl.col(color_col) == group_val)
                sx = self._resolve_x(subset, aes, x_cat_map)
                sy = subset[aes.y].to_list() if aes.y else list(range(len(subset)))
                color = color_map.get(str(group_val), "#333333")
                ax.scatter(
                    sx,
                    sy,
                    s=self.size**2,  # matplotlib uses area, not radius
                    c=color,
                    alpha=self.alpha,
                    marker=self.marker,
                    label=str(group_val),
                    zorder=3,
                    **self.kwargs,
                )
        else:
            x_values = self._resolve_x(data, aes, x_cat_map)
            y_values = data[aes.y].to_list() if aes.y else list(range(len(data)))
            ax.scatter(
                x_values,
                y_values,
                s=self.size**2,
                alpha=self.alpha,
                marker=self.marker,
                zorder=3,
                **self.kwargs,
            )
