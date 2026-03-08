"""Theme dataclass and default preset."""

from __future__ import annotations

import re
from typing import Literal

from matplotlib.axes import Axes
from pydantic import ConfigDict, field_validator
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(frozen=True))
class Theme:
    """Visual theme controlling axes, fonts, grid, and legend appearance."""

    font_family: str = "sans-serif"
    base_size: float = 7.0
    ink_color: str = "#000000"
    paper_color: str = "#FFFFFF"
    legend_position: Literal["right", "left", "top", "bottom", "none"] = "right"
    legend_title: str | None = None

    # Panel
    panel_background: str = "#FFFFFF"
    panel_grid_major: bool = True
    panel_grid_minor: bool = False
    panel_border: bool = False

    # Axes
    axis_line_x: bool = True
    axis_line_y: bool = True
    axis_ticks_x: bool = True
    axis_ticks_y: bool = True
    axis_labels_x: bool = True
    axis_labels_y: bool = True

    @field_validator("base_size")
    @classmethod
    def positive_base_size(cls, v: float) -> float:
        """Ensure base_size is strictly positive."""
        if v <= 0:
            raise ValueError(f"base_size must be positive, got {v}")
        return v

    @field_validator("ink_color", "paper_color", "panel_background")
    @classmethod
    def valid_hex_color(cls, v: str) -> str:
        """Ensure color fields are valid 6-digit hex strings."""
        if not re.match(r"^#[0-9a-fA-F]{6}$", v):
            raise ValueError(f"Expected a hex color like '#RRGGBB', got '{v!r}'")
        return v

    def apply(self, ax: Axes) -> None:
        """Apply this theme to a matplotlib Axes.

        Args:
            ax: The matplotlib Axes to style.
        """
        ink = self.ink_color
        ax.set_facecolor(self.paper_color)

        # Spines — hide all, then show selectively
        for spine in ax.spines.values():
            spine.set_visible(False)
        if self.axis_line_x:
            ax.spines["bottom"].set_visible(True)
            ax.spines["bottom"].set_color(ink)
        if self.axis_line_y:
            ax.spines["left"].set_visible(True)
            ax.spines["left"].set_color(ink)

        # Spine linewidth
        for spine in ax.spines.values():
            spine.set_linewidth(0.6)

        # Grid — subtle dashed lines, y-axis only
        ax.grid(
            self.panel_grid_major,
            which="major",
            axis="y",
            linestyle="--",
            linewidth=0.5,
            alpha=0.3,
        )

        # Y-axis breathing room
        ax.margins(y=0.05)

        # Tick styling
        ax.tick_params(
            labelsize=self.base_size,
            colors=ink,
            direction="out",
            width=0.6,
            length=3,
        )
        if not self.axis_ticks_x:
            ax.tick_params(axis="x", length=0)
        if not self.axis_ticks_y:
            ax.tick_params(axis="y", length=0)
        if not self.axis_labels_x:
            ax.set_xticklabels([])
        if not self.axis_labels_y:
            ax.set_yticklabels([])

        # Font
        for item in [ax.title, ax.xaxis.label, ax.yaxis.label]:
            item.set_fontfamily(self.font_family)
            item.set_fontsize(self.base_size)
            item.set_color(ink)


# The default theme — clean, minimal, publication-ready
THEME_PLOTCRAFT = Theme()
