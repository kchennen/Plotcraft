"""PlotCraft — the user-facing fluent API."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import matplotlib.pyplot as plt

from plotcraft.colors.palettes import ColorScheme
from plotcraft.core.spec import PlotSpec

# Unit conversion for adjust_size
_UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "in": 25.4}


class PlotCraft:
    """Fluent, chainable API for building publication-quality plots.

    Every method returns a **new** PlotCraft instance. The original
    is never mutated (immutable copy pattern).
    """

    __slots__ = ("_spec",)

    def __init__(self, spec: PlotSpec) -> None:
        """Initialize with a PlotSpec."""
        self._spec = spec

    # --- Internal helpers ---
    def _evolve(self, **changes: Any) -> PlotCraft:  # noqa: ANN401
        """Create a new PlotCraft with updated spec fields."""
        new_spec = replace(self._spec, **changes)
        return PlotCraft(new_spec)

    def _add_history(self, name: str) -> PlotSpec:
        """Return spec with a history breadcrumb appended."""
        return replace(self._spec, history=(*self._spec.history, name))

    # --- add_* methods ---
    # Lazy-imported inside methods to avoid circular imports
    def add_data_points(self, size: float = 2.0, alpha: float = 1.0, **kwargs: Any) -> PlotCraft:  # noqa: ANN401
        """Add a scatter layer showing individual data points."""
        from plotcraft.core.layer import Layer
        from plotcraft.geoms.point import GeomPoint
        from plotcraft.positions.identity import PositionIdentity
        from plotcraft.stats.identity import StatIdentity

        layer = Layer(
            geom=GeomPoint(size=size, alpha=alpha, **kwargs),
            stat=StatIdentity(),
            position=PositionIdentity(),
        )
        new_spec = self._add_history("add_data_points")
        return PlotCraft(replace(new_spec, layers=(*new_spec.layers, layer)))

    def add_title(self, title: str) -> PlotCraft:
        """Add a plot title."""
        return self._evolve(
            title=title,
            history=(*self._spec.history, "add_title"),
        )

    def add_caption(self, caption: str) -> PlotCraft:
        """Add a caption below the plot."""
        return self._evolve(
            caption=caption,
            history=(*self._spec.history, "add_caption"),
        )

    # --- adjust_* methods ---
    def adjust_colors(self, colors: ColorScheme | list[str] | dict[str, str]) -> PlotCraft:
        """Change the color palette.

        Args:
            colors: A ColorScheme, list of hex strings, or dict mapping
                    category names to hex colors.
        """
        if isinstance(colors, ColorScheme):
            return self._evolve(color_scheme=colors)
        elif isinstance(colors, dict):
            return self._evolve(color_map_override=colors)
        elif isinstance(colors, list):
            return self._evolve(color_scheme=ColorScheme.from_hex_list(colors))
        raise TypeError(f"Expected ColorScheme, list, or dict, got {type(colors).__name__}")

    def adjust_size(
        self,
        width: float | None = None,
        height: float | None = None,
        units: str = "mm",
    ) -> PlotCraft:
        """Change figure dimensions.

        Args:
            width: Figure width in the given units.
            height: Figure height in the given units.
            units: "mm" (default), "cm", or "in".
        """
        scale = _UNIT_TO_MM[units]
        changes: dict[str, Any] = {}
        if width is not None:
            changes["width_mm"] = width * scale
        if height is not None:
            changes["height_mm"] = height * scale
        return self._evolve(**changes)

    # --- remove_* methods ---
    def remove_legend(self) -> PlotCraft:
        """Hide the legend."""
        return self._evolve(theme=replace(self._spec.theme, legend_position="none"))

    def remove_x_axis_title(self) -> PlotCraft:
        """Remove the x-axis title."""
        return self._evolve(x_title="")

    def remove_y_axis_title(self) -> PlotCraft:
        """Remove the y-axis title."""
        return self._evolve(y_title="")

    # --- Terminal methods ---
    def render(self) -> tuple[Any, Any]:
        """Render the plot and return (Figure, Axes).

        This is the advanced escape hatch. It breaks the chain —
        the return type is a matplotlib tuple, not PlotCraft.
        """
        from plotcraft.render.engine import RenderEngine

        engine = RenderEngine()
        return engine.render(self._spec)

    def save_plot(
        self,
        path: str,
        width: float | None = None,
        height: float | None = None,
        units: str = "mm",
        dpi: int = 300,
    ) -> PlotCraft:
        """Render and save the plot to a file.

        Returns self to enable continued chaining (e.g., saving to
        multiple formats).
        """
        from plotcraft.render.engine import RenderEngine

        spec = self._spec
        if width is not None or height is not None:
            scale = _UNIT_TO_MM.get(units, 1.0)
            spec = replace(
                spec,
                width_mm=width * scale if width else spec.width_mm,
                height_mm=height * scale if height else spec.height_mm,
            )

        engine = RenderEngine()
        fig, _ax = engine.render(spec)
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return self

    def view_plot(self) -> PlotCraft:
        """Render and display the plot interactively.

        Returns self to enable continued chaining.
        """
        from plotcraft.render.engine import RenderEngine

        engine = RenderEngine()
        _fig, _ax = engine.render(self._spec)
        plt.show()
        return self

    # --- Dunder methods ---
    def __repr__(self) -> str:
        """Informative string representation showing layer count and history."""
        n_layers = len(self._spec.layers)
        history = " -> ".join(self._spec.history) if self._spec.history else "(empty)"
        return f"PlotCraft(layers={n_layers}, history=[{history}])"
