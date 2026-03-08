"""Tests for Theme validation and defaults."""

from __future__ import annotations

from dataclasses import replace

import pytest
from pydantic import ValidationError

from plotcraft.themes.base import THEME_PLOTCRAFT, Theme

# ── Default construction ──────────────────────────────────────────────────────


def test_theme_default_is_valid() -> None:
    """Theme() constructs successfully with all defaults."""
    t = Theme()
    assert t.legend_position == "right"
    assert t.base_size == pytest.approx(7.0)
    assert t.ink_color == "#000000"
    assert t.paper_color == "#FFFFFF"
    assert t.panel_background == "#FFFFFF"


def test_theme_plotcraft_constant_is_valid() -> None:
    """The module-level THEME_PLOTCRAFT constant is a valid Theme."""
    assert isinstance(THEME_PLOTCRAFT, Theme)
    assert THEME_PLOTCRAFT.legend_position == "right"


# ── legend_position validation ────────────────────────────────────────────────


@pytest.mark.parametrize("pos", ["right", "left", "top", "bottom", "none"])
def test_theme_valid_legend_positions(pos: str) -> None:
    """All five documented legend positions are accepted."""
    t = Theme(legend_position=pos)  # type: ignore[arg-type]
    assert t.legend_position == pos


@pytest.mark.parametrize("bad_pos", ["centre", "center", "Right", "NONE", "", " "])
def test_theme_rejects_invalid_legend_position(bad_pos: str) -> None:
    """Legend positions outside the allowed Literal raise ValidationError."""
    with pytest.raises(ValidationError, match="legend_position"):
        Theme(legend_position=bad_pos)  # type: ignore[arg-type]


# ── base_size validation ──────────────────────────────────────────────────────


def test_theme_rejects_zero_base_size() -> None:
    """base_size=0 raises ValidationError."""
    with pytest.raises(ValidationError, match="base_size"):
        Theme(base_size=0.0)


def test_theme_rejects_negative_base_size() -> None:
    """Negative base_size raises ValidationError."""
    with pytest.raises(ValidationError, match="base_size"):
        Theme(base_size=-4.0)


def test_theme_accepts_small_positive_base_size() -> None:
    """Any strictly positive base_size is accepted."""
    t = Theme(base_size=0.5)
    assert t.base_size == pytest.approx(0.5)


# ── Color field validation ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "field,value",
    [
        ("ink_color", "red"),  # named color — not hex
        ("ink_color", "#GGG000"),  # invalid hex digits
        ("ink_color", "#12345"),  # too short (5 chars)
        ("ink_color", "#1234567"),  # too long (7 chars)
        ("paper_color", "white"),
        ("panel_background", "rgb(0,0,0)"),
    ],
)
def test_theme_rejects_invalid_hex_colors(field: str, value: str) -> None:
    """Non-#RRGGBB strings in color fields raise ValidationError."""
    with pytest.raises(ValidationError):
        Theme(**{field: value})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "hex_color",
    [
        "#000000",
        "#FFFFFF",
        "#E64B35",
        "#aabbcc",
        "#AbCdEf",
    ],
)
def test_theme_accepts_valid_hex_colors(hex_color: str) -> None:
    """Valid 6-digit hex strings are accepted for color fields."""
    t = Theme(ink_color=hex_color)
    assert t.ink_color.lower() == hex_color.lower()


# ── Immutability (pydantic frozen=True) ──────────────────────────────────────


def test_theme_is_immutable() -> None:
    """Assigning to a frozen Theme raises an error."""
    t = Theme()
    with pytest.raises(Exception):  # pydantic raises ValidationError or AttributeError
        t.base_size = 99.0  # type: ignore[misc]


def test_theme_replace_is_validated() -> None:
    """dataclasses.replace() on a Theme validates the new value."""
    t = Theme()
    t2 = replace(t, base_size=10.0)
    assert t2.base_size == pytest.approx(10.0)
    # Invalid replacement should also be rejected
    with pytest.raises((ValidationError, TypeError, ValueError)):
        replace(t, legend_position="invalid")  # type: ignore[arg-type]
