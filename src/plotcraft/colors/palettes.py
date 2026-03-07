"""ColorScheme class and the default palette."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from plotcraft.colors.utils import apply_saturation, interpolate_colors


@dataclass(frozen=True, slots=True)
class ColorScheme:
    """A named collection of colors for mapping categorical/continuous data.

    Three palette types are supported:
    - "discrete": finite set of distinct colors (e.g., 7 friendly colors)
    - "continuous": anchor colors interpolated to any n (e.g., viridis)
    - "diverging": like continuous but symmetric around a midpoint (e.g., blue2red)

    For discrete palettes, get_colors(n) subsamples when n <= base count and
    interpolates when n exceeds the base count. For continuous/diverging palettes,
    get_colors always interpolates for smooth gradients.
    """

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
        # Discrete palettes subsample when we have enough base colors
        if self.palette_type == "discrete" and n <= len(self.colors):
            return list(self.colors[:n])
        # Everything else goes through interpolation
        return interpolate_colors(self.colors, n)

    def with_saturation(self, s: float) -> ColorScheme:
        """Return a new ColorScheme with saturation adjusted.

        Args:
            s: Saturation multiplier. 0.0 = grey, 1.0 = original, >1.0 = boosted.

        Returns:
            A new ColorScheme with each color adjusted.
        """
        adjusted = tuple(apply_saturation(c, s) for c in self.colors)
        return ColorScheme(
            name=f"{self.name}_s{s:.1f}",
            colors=adjusted,
            palette_type=self.palette_type,
        )

    def reversed(self) -> ColorScheme:
        """Return a new ColorScheme with reversed color order.

        Returns:
            A new ColorScheme with colors in reverse order.
        """
        return ColorScheme(
            name=f"{self.name}_r",
            colors=self.colors[::-1],
            palette_type=self.palette_type,
        )

    @staticmethod
    def from_hex_list(colors: list[str]) -> ColorScheme:
        """Create a ColorScheme from a list of hex strings.

        Args:
            colors: List of hex color strings.  Must be non-empty.

        Returns:
            A new ColorScheme with the given colors.

        Raises:
            ValueError: If ``colors`` is empty.
        """
        if not colors:
            raise ValueError("colors must be non-empty")
        return ColorScheme(name="custom", colors=tuple(colors))


def new_color_scheme(
    name: str,
    colors: list[str],
    palette_type: Literal["discrete", "continuous", "diverging"] = "discrete",
) -> ColorScheme:
    """Factory function for creating custom color schemes.

    This is the public API for users who want to define their own palettes:

        my_palette = pc.new_color_scheme("my_blues", ["#08306B", "#2171B5", "#6BAED6"])

    Args:
        name: A descriptive name for the scheme.
        colors: List of hex color strings (anchor colors).  Must be non-empty.
        palette_type: One of "discrete", "continuous", "diverging".

    Returns:
        A new ColorScheme instance.

    Raises:
        ValueError: If ``colors`` is empty.
    """
    if not colors:
        raise ValueError("colors must be non-empty")
    return ColorScheme(name=name, colors=tuple(colors), palette_type=palette_type)
