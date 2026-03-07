"""Diverging color palettes — symmetric around a midpoint for difference data."""

from __future__ import annotations

from plotcraft.colors.palettes import ColorScheme

colors_diverging_blue2red = ColorScheme(
    name="blue2red",
    colors=("#2166AC", "#67A9CF", "#D1E5F0", "#F7F7F7", "#FDDBC7", "#EF8A62", "#B2182B"),
    palette_type="diverging",
)

colors_diverging_blue2brown = ColorScheme(
    name="blue2brown",
    colors=("#01665E", "#5AB4AC", "#C7EAE5", "#F5F5F5", "#F6E8C3", "#D8B365", "#8C510A"),
    palette_type="diverging",
)

colors_diverging_spectral = ColorScheme(
    name="spectral",
    colors=("#D53E4F", "#FC8D59", "#FEE08B", "#FFFFBF", "#E6F598", "#99D594", "#3288BD"),
    palette_type="diverging",
)

colors_diverging_icefire = ColorScheme(
    name="icefire",
    colors=("#3B4CC0", "#7092F3", "#AAC7FD", "#F7F7F7", "#F9B397", "#E25749", "#B40426"),
    palette_type="diverging",
)

colors_diverging_BuRd = ColorScheme(  # noqa: N816
    name="BuRd",
    colors=("#2166AC", "#4393C3", "#92C5DE", "#F7F7F7", "#F4A582", "#D6604D", "#B2182B"),
    palette_type="diverging",
)

colors_diverging_BuYlRd = ColorScheme(  # noqa: N816
    name="BuYlRd",
    colors=("#313695", "#4575B4", "#ABD9E9", "#FFFFBF", "#FEE090", "#F46D43", "#A50026"),
    palette_type="diverging",
)
