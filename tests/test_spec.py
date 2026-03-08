"""Tests for PlotSpec immutability and validation."""

from dataclasses import replace

import polars as pl
import pytest

from plotcraft.core.aes import Aes
from plotcraft.core.spec import PlotSpec

# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_spec(**kwargs: object) -> PlotSpec:
    """Return a minimal PlotSpec, optionally overriding fields."""
    return PlotSpec(data=pl.DataFrame({"x": [1]}), aes=Aes(x="x"), **kwargs)  # type: ignore[arg-type]


# ── Immutability ──────────────────────────────────────────────────────────────


def test_plotspec_is_frozen() -> None:
    """Assigning to a frozen PlotSpec raises AttributeError."""
    spec = _make_spec()
    try:
        spec.title = "new"  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"
    except AttributeError:
        pass


def test_plotspec_replace_creates_new_instance() -> None:
    """dataclasses.replace returns a new spec without mutating the original."""
    spec = _make_spec()
    new_spec = replace(spec, title="Hello")
    assert new_spec.title == "Hello"
    assert spec.title == ""  # original unchanged


def test_plotspec_layers_are_tuples() -> None:
    """Layers default to an empty tuple for immutability."""
    spec = _make_spec()
    assert isinstance(spec.layers, tuple)


# ── Dimension validation ──────────────────────────────────────────────────────


def test_plotspec_rejects_negative_width_mm() -> None:
    """PlotSpec raises ValueError when width_mm is negative."""
    with pytest.raises(ValueError, match="width_mm"):
        _make_spec(width_mm=-10.0)


def test_plotspec_rejects_zero_width_mm() -> None:
    """PlotSpec raises ValueError when width_mm is zero."""
    with pytest.raises(ValueError, match="width_mm"):
        _make_spec(width_mm=0.0)


def test_plotspec_rejects_negative_height_mm() -> None:
    """PlotSpec raises ValueError when height_mm is negative."""
    with pytest.raises(ValueError, match="height_mm"):
        _make_spec(height_mm=-5.0)


def test_plotspec_rejects_zero_height_mm() -> None:
    """PlotSpec raises ValueError when height_mm is zero."""
    with pytest.raises(ValueError, match="height_mm"):
        _make_spec(height_mm=0.0)


def test_plotspec_accepts_positive_dimensions() -> None:
    """PlotSpec accepts any strictly positive width and height."""
    spec = _make_spec(width_mm=0.1, height_mm=0.1)
    assert spec.width_mm == pytest.approx(0.1)
    assert spec.height_mm == pytest.approx(0.1)


# ── dodge_width validation ────────────────────────────────────────────────────


def test_plotspec_rejects_zero_dodge_width() -> None:
    """PlotSpec raises ValueError when dodge_width is zero."""
    with pytest.raises(ValueError, match="dodge_width"):
        _make_spec(dodge_width=0.0)


def test_plotspec_rejects_negative_dodge_width() -> None:
    """PlotSpec raises ValueError when dodge_width is negative."""
    with pytest.raises(ValueError, match="dodge_width"):
        _make_spec(dodge_width=-0.5)


def test_plotspec_rejects_excessive_dodge_width() -> None:
    """PlotSpec raises ValueError when dodge_width exceeds 2."""
    with pytest.raises(ValueError, match="dodge_width"):
        _make_spec(dodge_width=2.1)


def test_plotspec_accepts_boundary_dodge_width() -> None:
    """PlotSpec accepts dodge_width exactly at the upper boundary (2.0)."""
    spec = _make_spec(dodge_width=2.0)
    assert spec.dodge_width == 2.0


# ── padding validation ────────────────────────────────────────────────────────


def test_plotspec_rejects_wrong_padding_length() -> None:
    """PlotSpec raises ValueError when padding does not have exactly 4 values."""
    with pytest.raises(ValueError, match="padding"):
        _make_spec(padding=(0.05, 0.05, 0.05))  # type: ignore[arg-type]


def test_plotspec_rejects_padding_out_of_range() -> None:
    """PlotSpec raises ValueError when any padding value is outside [0, 1]."""
    with pytest.raises(ValueError, match="padding"):
        _make_spec(padding=(0.05, 0.05, 0.05, 1.1))


def test_plotspec_accepts_valid_padding() -> None:
    """PlotSpec accepts a 4-element padding tuple with all values in [0, 1]."""
    spec = _make_spec(padding=(0.0, 0.5, 1.0, 0.25))
    assert spec.padding == (0.0, 0.5, 1.0, 0.25)
