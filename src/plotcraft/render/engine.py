"""RenderEngine — the rendering pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from plotcraft.core.spec import PlotSpec


class RenderEngine:
    """Renders a PlotSpec into a matplotlib Figure + Axes."""

    def render(self, spec: PlotSpec) -> tuple[Figure, Axes]:
        """Execute the full rendering pipeline.

        Args:
            spec: The PlotSpec describing data, layers, and theme.

        Returns:
            A (Figure, Axes) tuple with the rendered plot.
        """
        fig, ax = self._create_figure(spec)

        # Apply theme
        spec.theme.apply(ax)

        # Build color map — spread directly so geoms see the correct keys:
        # discrete → {"color_map": {val: hex, …}}
        # continuous → {"colormap": Colormap, "norm": Normalize, "continuous": True}
        scales: dict[str, Any] = {**self._build_color_map(spec)}

        # Build categorical axis map (if x column is non-numeric)
        x_cat_map = self._build_category_map(spec)
        if x_cat_map:
            scales["x_cat_map"] = x_cat_map

        # Render each layer
        for layer in spec.layers:
            aes = layer.resolve_aes(spec.aes)
            data = layer.data if layer.data is not None else spec.data
            computed = layer.compute(data, aes)
            layer.geom.draw(ax, computed, aes, scales, spec.theme)

        # Apply categorical axis ticks after geoms have drawn
        if x_cat_map:
            self._apply_category_axis(ax, x_cat_map)

        # Apply titles
        self._apply_titles(ax, spec)

        # Apply legend
        self._apply_legend(ax, spec)

        fig.tight_layout()
        return fig, ax

    def _create_figure(self, spec: PlotSpec) -> tuple[Figure, Axes]:
        """Create figure with dimensions converted from mm to inches.

        Args:
            spec: The PlotSpec whose width/height (mm) determine figure size.

        Returns:
            A (Figure, Axes) tuple sized to the spec dimensions.
        """
        w_in = spec.width_mm / 25.4
        h_in = spec.height_mm / 25.4
        fig, ax = plt.subplots(figsize=(w_in, h_in))
        return fig, ax

    def _build_color_map(self, spec: PlotSpec) -> dict[str, Any]:
        """Map color-column values to colors.

        Args:
            spec: The PlotSpec whose aes.color or aes.fill column is inspected.

        Returns a dict with either:
        - {"color_map": {val: hex, ...}} for discrete data
        - {"colormap": Colormap, "norm": Normalize, "continuous": True} for continuous data
        """
        # If user provided an explicit override, use it
        if spec.color_map_override:
            return {"color_map": spec.color_map_override}

        color_col = spec.aes.color or spec.aes.fill
        if color_col is None or color_col not in spec.data.columns:
            return {}

        # Detect continuous: numeric column + continuous/diverging palette
        col_dtype = spec.data[color_col].dtype
        is_numeric = col_dtype.is_numeric()
        is_continuous_palette = spec.color_scheme.palette_type in ("continuous", "diverging")

        if is_numeric and is_continuous_palette:
            import matplotlib.colors as mcolors
            import numpy as np

            values = spec.data[color_col].to_numpy()
            vmin, vmax = float(np.nanmin(values)), float(np.nanmax(values))

            if spec.color_scheme.palette_type == "diverging":
                abs_max = max(abs(vmin), abs(vmax))
                norm = mcolors.Normalize(vmin=-abs_max, vmax=abs_max)
            else:
                norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

            cmap = mcolors.LinearSegmentedColormap.from_list(
                spec.color_scheme.name,
                list(spec.color_scheme.colors),
                N=256,
            )
            return {"colormap": cmap, "norm": norm, "continuous": True}

        # Discrete path
        unique_vals = spec.data[color_col].unique().sort().to_list()
        colors = spec.color_scheme.get_colors(len(unique_vals))
        return {"color_map": {str(v): c for v, c in zip(unique_vals, colors)}}

    def _build_category_map(
        self,
        spec: PlotSpec,
    ) -> dict[str, int]:
        """Build a string→int mapping for categorical x-axis columns.

        Args:
            spec: The PlotSpec whose x aesthetic column is inspected.

        Returns:
            A dict mapping category strings to integer tick positions,
            or an empty dict if x is numeric or not set.
        """
        x_col = spec.aes.x
        if x_col is None or x_col not in spec.data.columns:
            return {}

        dtype = spec.data[x_col].dtype
        if dtype.is_numeric():
            return {}

        categories = spec.data[x_col].unique().sort().to_list()
        return {str(v): i for i, v in enumerate(categories)}

    def _apply_category_axis(
        self,
        ax: Axes,
        x_cat_map: dict[str, int],
    ) -> None:
        """Set tick positions and labels for a categorical x-axis.

        Args:
            ax: The matplotlib Axes to configure.
            x_cat_map: Mapping of category names to integer positions.
        """
        labels = list(x_cat_map.keys())
        positions = list(x_cat_map.values())
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.margins(x=0.15)

    def _apply_titles(self, ax: Axes, spec: PlotSpec) -> None:
        """Set title, caption, and axis labels.

        Args:
            ax: The matplotlib Axes to annotate.
            spec: The PlotSpec containing title, axis titles, and caption.
        """
        if spec.title:
            ax.set_title(
                spec.title,
                fontsize=spec.theme.base_size + 1,
                fontweight="bold",
                pad=6,
            )

        # X-axis title
        if spec.x_title is not None:
            ax.set_xlabel(spec.x_title, fontsize=spec.theme.base_size)
        elif spec.aes.x:
            ax.set_xlabel(spec.aes.x, fontsize=spec.theme.base_size)

        # Y-axis title
        if spec.y_title is not None:
            ax.set_ylabel(spec.y_title, fontsize=spec.theme.base_size)
        elif spec.aes.y:
            ax.set_ylabel(spec.aes.y, fontsize=spec.theme.base_size)

        # Caption as figure text (below the axes)
        if spec.caption:
            ax.figure.text(
                0.5,
                0.01,
                spec.caption,
                ha="center",
                fontsize=spec.theme.base_size - 1,
                style="italic",
            )

    def _apply_legend(self, ax: Axes, spec: PlotSpec) -> None:
        """Show or hide the legend based on theme settings.

        Args:
            ax: The matplotlib Axes containing legend handles.
            spec: The PlotSpec whose theme controls legend placement.
        """
        if spec.theme.legend_position == "none":
            legend = ax.get_legend()
            if legend:
                legend.remove()
            return

        handles, labels = ax.get_legend_handles_labels()
        if not handles:
            return

        loc_map = {
            "right": "center left",
            "left": "center right",
            "top": "lower center",
            "bottom": "upper center",
        }
        bbox_map = {
            "right": (1.02, 0.5),
            "left": (-0.15, 0.5),
            "top": (0.5, 1.15),
            "bottom": (0.5, -0.15),
        }

        pos = spec.theme.legend_position
        ax.legend(
            handles,
            labels,
            loc=loc_map.get(pos, "best"),
            bbox_to_anchor=bbox_map.get(pos),
            fontsize=spec.theme.base_size,
            title=spec.theme.legend_title,
            frameon=False,
        )
