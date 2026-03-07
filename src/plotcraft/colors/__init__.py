"""Color system — palettes, utilities, and the ColorScheme class."""

# --- Continuous ---
from plotcraft.colors.continuous import (
    colors_continuous_bluepinkyellow,
    colors_continuous_cividis,
    colors_continuous_inferno,
    colors_continuous_magma,
    colors_continuous_mako,
    colors_continuous_plasma,
    colors_continuous_rocket,
    colors_continuous_turbo,
    colors_continuous_viridis,
)

# --- Discrete ---
from plotcraft.colors.discrete import (
    colors_discrete_alger,
    colors_discrete_apple,
    colors_discrete_candy,
    colors_discrete_friendly,
    colors_discrete_friendly_long,
    colors_discrete_ibm,
    colors_discrete_metro,
    colors_discrete_okabeito,
    colors_discrete_rainbow,
    colors_discrete_seaside,
    colors_discrete_tableau10,
    colors_discrete_tol_light,
    colors_discrete_tol_muted,
    colors_discrete_tol_vibrant,
    colors_discrete_wong,
)

# --- Diverging ---
from plotcraft.colors.diverging import (
    colors_diverging_blue2brown,
    colors_diverging_blue2red,
    colors_diverging_BuRd,
    colors_diverging_BuYlRd,
    colors_diverging_icefire,
    colors_diverging_spectral,
)

# --- Journal ---
from plotcraft.colors.journal import (
    colors_journal_aaas,
    colors_journal_d3,
    colors_journal_igv,
    colors_journal_jama,
    colors_journal_lancet,
    colors_journal_nejm,
    colors_journal_npg,
)
from plotcraft.colors.palettes import ColorScheme as ColorScheme
from plotcraft.colors.palettes import new_color_scheme as new_color_scheme

__all__ = [
    "ColorScheme",
    "colors_continuous_bluepinkyellow",
    "colors_continuous_cividis",
    "colors_continuous_inferno",
    "colors_continuous_magma",
    "colors_continuous_mako",
    "colors_continuous_plasma",
    "colors_continuous_rocket",
    "colors_continuous_turbo",
    # Continuous (9)
    "colors_continuous_viridis",
    "colors_discrete_alger",
    "colors_discrete_apple",
    "colors_discrete_candy",
    # Discrete (15)
    "colors_discrete_friendly",
    "colors_discrete_friendly_long",
    "colors_discrete_ibm",
    "colors_discrete_metro",
    "colors_discrete_okabeito",
    "colors_discrete_rainbow",
    "colors_discrete_seaside",
    "colors_discrete_tableau10",
    "colors_discrete_tol_light",
    "colors_discrete_tol_muted",
    "colors_discrete_tol_vibrant",
    "colors_discrete_wong",
    "colors_diverging_BuRd",
    "colors_diverging_BuYlRd",
    "colors_diverging_blue2brown",
    # Diverging (6)
    "colors_diverging_blue2red",
    "colors_diverging_icefire",
    "colors_diverging_spectral",
    "colors_journal_aaas",
    "colors_journal_d3",
    "colors_journal_igv",
    "colors_journal_jama",
    "colors_journal_lancet",
    "colors_journal_nejm",
    # Journal (7)
    "colors_journal_npg",
    "new_color_scheme",
]
