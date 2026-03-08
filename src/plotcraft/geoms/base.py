"""Base class for all geometries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import polars as pl
from matplotlib.axes import Axes

from plotcraft.core.aes import Aes


class Geom(ABC):
    """Abstract geometry — knows how to draw data onto an Axes."""

    @abstractmethod
    def draw(
        self,
        ax: Axes,
        data: pl.DataFrame,
        aes: Aes,
        scales: dict[str, Any],
        theme: Any,  # noqa: ANN401
    ) -> None:
        """Draw this geometry onto the given matplotlib Axes.

        Args:
            ax: The matplotlib Axes to draw on.
            data: The data to visualize.
            aes: The resolved aesthetic mapping.
            scales: A dict of precomputed scale information (e.g. color_map).
            theme: The active theme controlling visual style.
        """
        ...

    # ── Shared x-axis helpers ─────────────────────────────────────────────────

    @staticmethod
    def _resolve_x(
        data: pl.DataFrame,
        aes: Aes,
        x_cat_map: dict[str, int],
    ) -> list[int] | list[Any]:
        """Return x positions for every row in *data*.

        Uses O(1) dict lookup from *x_cat_map* when the x column is
        categorical; falls through to the raw column values for numeric x.

        Args:
            data: The (possibly filtered) DataFrame to resolve positions for.
            aes: Aesthetic mapping whose ``.x`` field names the x column.
            x_cat_map: String-to-integer position map built by the engine;
                empty when x is numeric.

        Returns:
            A list of integer positions (categorical) or raw values (numeric).
        """
        if not aes.x:
            return list(range(len(data)))
        raw = data[aes.x].to_list()
        if x_cat_map:
            return [x_cat_map[str(v)] for v in raw]
        return raw

    @staticmethod
    def _resolve_x_grouped(
        x_vals: list[Any],
        x_cat_map: dict[str, int],
        group_index: int,
        n_groups: int,
        group_width: float,
    ) -> list[float]:
        """Compute x positions for one group in a side-by-side layout.

        Avoids the O(n) ``list.index()`` call: when *x_cat_map* is present
        each lookup is O(1). For numeric x (empty *x_cat_map*) the raw
        values are used directly as positions.

        Args:
            x_vals: Raw x values for this group.
            x_cat_map: String-to-integer position map (empty for numeric x).
            group_index: Zero-based index of this group among all groups.
            n_groups: Total number of groups (for centering the offset).
            group_width: Width allocated to each individual group's element.

        Returns:
            A list of float x positions with the group offset applied.
        """
        offset = (group_index - (n_groups - 1) / 2) * group_width
        if x_cat_map:
            return [x_cat_map[str(v)] + offset for v in x_vals]
        return [float(v) + offset for v in x_vals]  # type: ignore[arg-type]

    @staticmethod
    def _apply_x_ticks(
        ax: Axes,
        labels: list[Any],
        x_cat_map: dict[str, int],
    ) -> None:
        """Set integer x-axis ticks with string labels.

        This is a **no-op** when *x_cat_map* is non-empty — in that case
        the render engine's ``_apply_category_axis()`` already handles
        ticks and labels after all geoms have drawn, so each geom must
        not overwrite them.

        Args:
            ax: The Axes to configure.
            labels: Original x values used as tick labels (only needed when
                the engine does not manage ticks, i.e. *x_cat_map* is empty).
            x_cat_map: String-to-integer position map; non-empty signals
                that the engine owns tick management.
        """
        if x_cat_map:
            return
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels([str(v) for v in labels])
