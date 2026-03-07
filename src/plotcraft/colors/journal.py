"""Journal-specific color palettes — inspired by ggsci."""

from __future__ import annotations

from plotcraft.colors.palettes import ColorScheme

# Nature Publishing Group (NPG)
colors_journal_npg = ColorScheme(
    name="npg",
    colors=(
        "#E64B35",
        "#4DBBD5",
        "#00A087",
        "#3C5488",
        "#F39B7F",
        "#8491B4",
        "#91D1C2",
        "#DC0000",
        "#7E6148",
        "#B09C85",
    ),
)

# The Lancet
colors_journal_lancet = ColorScheme(
    name="lancet",
    colors=("#00468B", "#ED0000", "#42B540", "#0099B4", "#925E9F", "#FDAF91", "#AD002A", "#ADB6B6"),
)

# New England Journal of Medicine
colors_journal_nejm = ColorScheme(
    name="nejm",
    colors=("#BC3C29", "#0072B5", "#E18727", "#20854E", "#7876B1", "#6F99AD", "#FFDC91", "#EE4C97"),
)

# JAMA
colors_journal_jama = ColorScheme(
    name="jama",
    colors=("#374E55", "#DF8F44", "#00A1D5", "#B24745", "#79AF97", "#6A6599", "#80796B"),
)

# AAAS (Science)
colors_journal_aaas = ColorScheme(
    name="aaas",
    colors=(
        "#3B4992",
        "#EE0000",
        "#008B45",
        "#631879",
        "#008280",
        "#BB0021",
        "#5F559B",
        "#A20056",
        "#808180",
        "#1B1919",
    ),
)

# D3.js category palette
colors_journal_d3 = ColorScheme(
    name="d3",
    colors=(
        "#1F77B4",
        "#FF7F0E",
        "#2CA02C",
        "#D62728",
        "#9467BD",
        "#8C564B",
        "#E377C2",
        "#7F7F7F",
        "#BCBD22",
        "#17BECF",
    ),
)

# Integrative Genomics Viewer (IGV)
colors_journal_igv = ColorScheme(
    name="igv",
    colors=(
        "#5050FF",
        "#CE3D32",
        "#749B58",
        "#F0E685",
        "#466983",
        "#BA6338",
        "#5DB1DD",
        "#802268",
        "#6BD76B",
        "#D595A7",
    ),
)
