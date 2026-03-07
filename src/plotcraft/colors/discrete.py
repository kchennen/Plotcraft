"""Discrete color palettes — 15 named schemes for categorical data."""

from __future__ import annotations

from plotcraft.colors.palettes import ColorScheme

# -------------------------------------------------------------------
# Discrete palettes (10)
# -------------------------------------------------------------------

colors_discrete_friendly = ColorScheme(
    name="friendly",
    colors=("#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB"),
)

colors_discrete_friendly_long = ColorScheme(
    name="friendly_long",
    colors=(
        "#4477AA",
        "#EE6677",
        "#228833",
        "#CCBB44",
        "#66CCEE",
        "#AA3377",
        "#BBBBBB",
        "#EE7733",
        "#0077BB",
        "#33BBEE",
        "#EE3377",
        "#CC3311",
        "#009988",
        "#DDCC77",
        "#882255",
    ),
)

colors_discrete_seaside = ColorScheme(
    name="seaside",
    colors=("#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02", "#A6761D"),
)

colors_discrete_apple = ColorScheme(
    name="apple",
    colors=("#FF3B30", "#FF9500", "#FFCC00", "#34C759", "#5AC8FA", "#007AFF", "#5856D6", "#AF52DE", "#FF2D55"),
)

colors_discrete_ibm = ColorScheme(
    name="ibm",
    colors=("#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000"),
)

colors_discrete_candy = ColorScheme(
    name="candy",
    colors=("#F8B195", "#F67280", "#C06C84", "#6C5B7B", "#355C7D", "#99B898", "#FECEAB"),
)

colors_discrete_alger = ColorScheme(
    name="alger",
    colors=("#E63946", "#F1FAEE", "#A8DADC", "#457B9D", "#1D3557"),
)

colors_discrete_metro = ColorScheme(
    name="metro",
    colors=("#D11141", "#00B159", "#00AEDB", "#F37735", "#FFC425"),
)

colors_discrete_okabeito = ColorScheme(
    name="okabeito",
    colors=("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"),
)

colors_discrete_rainbow = ColorScheme(
    name="rainbow",
    colors=("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", "#FFFF33", "#A65628", "#F781BF"),
)

# -------------------------------------------------------------------
# Additional discrete palettes (5)
# -------------------------------------------------------------------

colors_discrete_wong = ColorScheme(
    name="wong",
    colors=("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"),
)

colors_discrete_tableau10 = ColorScheme(
    name="tableau10",
    colors=(
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14F",
        "#EDC948",
        "#B07AA1",
        "#FF9DA7",
        "#9C755F",
        "#BAB0AC",
    ),
)

colors_discrete_tol_vibrant = ColorScheme(
    name="tol_vibrant",
    colors=("#EE7733", "#0077BB", "#33BBEE", "#EE3377", "#CC3311", "#009988", "#BBBBBB"),
)

colors_discrete_tol_muted = ColorScheme(
    name="tol_muted",
    colors=(
        "#CC6677",
        "#332288",
        "#DDCC77",
        "#117733",
        "#88CCEE",
        "#882255",
        "#44AA99",
        "#999933",
        "#AA4499",
    ),
)

colors_discrete_tol_light = ColorScheme(
    name="tol_light",
    colors=(
        "#77AADD",
        "#EE8866",
        "#EEDD88",
        "#FFAABB",
        "#99DDFF",
        "#44BB99",
        "#BBCC33",
        "#AAAA00",
        "#DDDDDD",
    ),
)
