"""Color utility functions — saturation and interpolation."""

from __future__ import annotations

import colorsys
import functools

import matplotlib.colors as mcolors


def apply_saturation(hex_color: str, saturation: float) -> str:
    """Adjust the saturation of a hex color.

    Args:
        hex_color: A hex color string (e.g., "#E64B35").
        saturation: Multiplier for saturation. 0.0 = fully desaturated (grey),
                    1.0 = original color. Values > 1.0 boost saturation, capped
                    at 1.0 (the maximum HSV saturation).

    Returns:
        A new hex color string with adjusted saturation.
    """
    r, g, b = mcolors.to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s = min(1.0, s * saturation)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    return mcolors.to_hex((r2, g2, b2))


@functools.lru_cache(maxsize=64)
def _build_colormap(colors: tuple[str, ...]) -> mcolors.LinearSegmentedColormap:
    """Build (and cache) a LinearSegmentedColormap from anchor colors.

    The result is memoised so repeated calls with the same palette avoid
    re-constructing the colormap on every get_colors() invocation.

    Args:
        colors: Anchor hex color strings as a hashable tuple.

    Returns:
        A matplotlib LinearSegmentedColormap ready for sampling.
    """
    return mcolors.LinearSegmentedColormap.from_list("interp", list(colors), N=256)


def interpolate_colors(colors: tuple[str, ...], n: int) -> list[str]:
    """Interpolate a palette to produce exactly n colors.

    Uses matplotlib's LinearSegmentedColormap for smooth interpolation.
    The colormap is cached per unique color tuple to avoid repeated
    construction when get_colors() is called multiple times on the same scheme.

    Args:
        colors: Base anchor colors as hex strings.  Must be non-empty.
        n: Number of output colors.

    Returns:
        List of n hex color strings.

    Raises:
        ValueError: If ``colors`` is empty.
    """
    if not colors:
        raise ValueError("colors must be a non-empty sequence")
    if n <= 0:
        return []
    if n == 1:
        return [colors[0]]
    cmap = _build_colormap(colors)
    return [mcolors.to_hex(cmap(i / max(1, n - 1))) for i in range(n)]
