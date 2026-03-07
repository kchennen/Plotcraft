"""Continuous color palettes — smooth gradients for numeric data."""

from __future__ import annotations

from plotcraft.colors.palettes import ColorScheme

# Anchors extracted from matplotlib colormaps at evenly spaced intervals.
# Using 5-7 anchor points gives excellent interpolation via LinearSegmentedColormap.

colors_continuous_viridis = ColorScheme(
    name="viridis",
    colors=("#440154", "#31688E", "#35B779", "#FDE725"),
    palette_type="continuous",
)

colors_continuous_magma = ColorScheme(
    name="magma",
    colors=("#000004", "#3B0F70", "#8C2981", "#DE4968", "#FE9F6D", "#FCFDBF"),
    palette_type="continuous",
)

colors_continuous_inferno = ColorScheme(
    name="inferno",
    colors=("#000004", "#420A68", "#932667", "#DD513A", "#FCA50A", "#FCFFA4"),
    palette_type="continuous",
)

colors_continuous_plasma = ColorScheme(
    name="plasma",
    colors=("#0D0887", "#6A00A8", "#B12A90", "#E16462", "#FCA636", "#F0F921"),
    palette_type="continuous",
)

colors_continuous_cividis = ColorScheme(
    name="cividis",
    colors=("#002051", "#255668", "#5C7B45", "#A69D35", "#FDEA45"),
    palette_type="continuous",
)

colors_continuous_rocket = ColorScheme(
    name="rocket",
    colors=("#03051A", "#4C1D6B", "#A11A5B", "#E3611C", "#FABD72", "#F6FADB"),
    palette_type="continuous",
)

colors_continuous_mako = ColorScheme(
    name="mako",
    colors=("#0B0405", "#3B0F6F", "#1E6E87", "#5BB982", "#DEF5E5"),
    palette_type="continuous",
)

colors_continuous_turbo = ColorScheme(
    name="turbo",
    colors=(
        "#30123B",
        "#4662D7",
        "#36AAF9",
        "#1AE4B6",
        "#72FE5E",
        "#C8EF34",
        "#FABA39",
        "#F66B19",
        "#A2FC3C",
        "#7A0403",
    ),
    palette_type="continuous",
)

colors_continuous_bluepinkyellow = ColorScheme(
    name="bluepinkyellow",
    colors=("#2166AC", "#67A9CF", "#D1E5F0", "#F7CFD0", "#EF8A62", "#FDDBC7", "#FEF0B1"),
    palette_type="continuous",
)
