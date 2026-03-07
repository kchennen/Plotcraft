"""Shared type aliases and protocols."""

from __future__ import annotations

from typing import Any, Literal

# Unit types for adjust_size
Units = Literal["mm", "cm", "in"]

# Palette type
PaletteType = Literal["discrete", "continuous", "diverging"]

# Re-export for convenience
__all__ = ["Any", "PaletteType", "Units"]
