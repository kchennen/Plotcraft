"""Color utility functions — saturation and interpolation."""

from __future__ import annotations

import colorsys

import matplotlib.colors as mcolors


def apply_saturation(hex_color: str, saturation: float) -> str:
    """Adjust the saturation of a hex color.

    Args:
        hex_color: A hex color string (e.g., "#E64B35").
        saturation: Multiplier for saturation. 0.0 = fully desaturated (grey),
                    1.0 = original color. Values > 1.0 boost saturation.

    Returns:
        A new hex color string with adjusted saturation.
    """
    r, g, b = mcolors.to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s = min(1.0, s * saturation)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    return mcolors.to_hex((r2, g2, b2))


def interpolate_colors(colors: tuple[str, ...], n: int) -> list[str]:
    """Interpolate a palette to produce exactly n colors.

    Uses matplotlib's LinearSegmentedColormap for smooth interpolation.
    This is the core function that makes palettes work at any size.

    Args:
        colors: Base anchor colors as hex strings.
        n: Number of output colors.

    Returns:
        List of n hex color strings.
    """
    if n <= 0:
        return []
    if n == 1:
        return [colors[0]]
    cmap = mcolors.LinearSegmentedColormap.from_list("interp", list(colors), N=256)
    return [mcolors.to_hex(cmap(i / max(1, n - 1))) for i in range(n)]
