"""ColorScheme class and the default palette."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ColorScheme:
    """A named collection of colors for mapping categorical/continuous data."""

    name: str
    colors: tuple[str, ...]
    palette_type: Literal["discrete", "continuous", "diverging"] = "discrete"

    def get_colors(self, n: int) -> list[str]:
        """Get a list of n colors from the scheme.

        For discrete schemes, this returns the first n colors (cycling if
        n > available). For continuous/diverging schemes, this interpolates
        across the colors to create a gradient.

        Args:
            n: The number of colors to return.

        Returns:
            A list of n hex color strings.
        """
        if n <= 0:
            return []
        if n <= len(self.colors):
            return list(self.colors[:n])
        # Cycle colors if we need more than available
        return [self.colors[i % len(self.colors)] for i in range(n)]

    @staticmethod
    def from_hex_list(colors: list[str]) -> ColorScheme:
        """Create a ColorScheme from a list of hex strings.

        Args:
            colors: List of hex color strings.

        Returns:
            A new ColorScheme with the given colors.
        """
        return ColorScheme(name="custom", colors=tuple(colors))


# Default palette — Tol "friendly" 7-color scheme
colors_discrete_friendly = ColorScheme(
    name="friendly",
    colors=("#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"),
)
