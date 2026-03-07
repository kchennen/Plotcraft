"""Global session-wide defaults."""

from __future__ import annotations

from dataclasses import dataclass, field

from plotcraft.colors.discrete import colors_discrete_friendly
from plotcraft.colors.palettes import ColorScheme
from plotcraft.themes.base import THEME_PLOTCRAFT, Theme


@dataclass
class _GlobalOptions:
    """Session-wide defaults read by the plotcraft() constructor."""

    theme: Theme = field(default_factory=lambda: THEME_PLOTCRAFT)
    color_scheme: ColorScheme = field(default_factory=lambda: colors_discrete_friendly)
    width: float = 50.0  # mm
    height: float = 50.0  # mm


# Module-level singleton
_OPTIONS = _GlobalOptions()


def get_options() -> _GlobalOptions:
    """Return the current global options (internal use).

    Returns:
        The module-level _GlobalOptions singleton.
    """
    return _OPTIONS
