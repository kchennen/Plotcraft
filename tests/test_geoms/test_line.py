"""Tests for GeomLine and GeomArea rendering and validation."""

from __future__ import annotations

import matplotlib.pyplot as plt
import polars as pl
import pytest

from plotcraft.core.aes import Aes
from plotcraft.geoms.line import GeomArea, GeomLine


class TestGeomLine:
    """Test line geometry."""

    def test_draws_without_error(self) -> None:
        """GeomLine.draw() completes without raising."""
        fig, ax = plt.subplots()
        data = pl.DataFrame({"x": [1.0, 2.0, 3.0], "y": [4.0, 5.0, 6.0]})
        geom = GeomLine()
        geom.draw(ax, data, Aes(x="x", y="y"), {}, None)
        plt.close(fig)

    def test_draws_with_color(self) -> None:
        """GeomLine handles discrete color grouping."""
        fig, ax = plt.subplots()
        data = pl.DataFrame(
            {
                "x": [1.0, 2.0, 1.0, 2.0],
                "y": [3.0, 4.0, 5.0, 6.0],
                "group": ["A", "A", "B", "B"],
            }
        )
        color_map = {"A": "#FF0000", "B": "#0000FF"}
        geom = GeomLine()
        geom.draw(
            ax,
            data,
            Aes(x="x", y="y", color="group"),
            {"color_map": color_map},
            None,
        )
        plt.close(fig)


class TestGeomLineValidation:
    """GeomLine rejects invalid constructor parameters."""

    def test_zero_linewidth_raises(self) -> None:
        """linewidth=0 raises ValueError."""
        with pytest.raises(ValueError, match="linewidth"):
            GeomLine(linewidth=0.0)

    def test_negative_linewidth_raises(self) -> None:
        """Negative linewidth raises ValueError."""
        with pytest.raises(ValueError, match="linewidth"):
            GeomLine(linewidth=-2.0)

    def test_alpha_above_one_raises(self) -> None:
        """Alpha > 1 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomLine(alpha=1.5)

    def test_negative_alpha_raises(self) -> None:
        """Alpha < 0 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomLine(alpha=-0.01)

    def test_boundary_alpha_values_accepted(self) -> None:
        """alpha=0.0 and alpha=1.0 are both valid."""
        GeomLine(alpha=0.0)
        GeomLine(alpha=1.0)

    def test_positive_linewidth_accepted(self) -> None:
        """Any positive linewidth is accepted."""
        g = GeomLine(linewidth=0.5)
        assert g.linewidth == pytest.approx(0.5)


class TestGeomArea:
    """Test filled area geometry."""

    def test_draws_without_error(self) -> None:
        """GeomArea.draw() completes without raising."""
        fig, ax = plt.subplots()
        data = pl.DataFrame({"x": [1.0, 2.0, 3.0], "y": [1.0, 4.0, 2.0]})
        geom = GeomArea()
        geom.draw(ax, data, Aes(x="x", y="y"), {}, None)
        plt.close(fig)

    def test_draws_with_color(self) -> None:
        """GeomArea handles discrete color grouping."""
        fig, ax = plt.subplots()
        data = pl.DataFrame(
            {
                "x": [1.0, 2.0, 1.0, 2.0],
                "y": [3.0, 4.0, 5.0, 6.0],
                "group": ["A", "A", "B", "B"],
            }
        )
        color_map = {"A": "#FF0000", "B": "#0000FF"}
        geom = GeomArea()
        geom.draw(
            ax,
            data,
            Aes(x="x", y="y", color="group"),
            {"color_map": color_map},
            None,
        )
        plt.close(fig)


class TestGeomAreaValidation:
    """GeomArea rejects invalid constructor parameters."""

    def test_alpha_above_one_raises(self) -> None:
        """Alpha > 1 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomArea(alpha=1.1)

    def test_negative_alpha_raises(self) -> None:
        """Alpha < 0 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomArea(alpha=-0.5)

    def test_boundary_alpha_values_accepted(self) -> None:
        """alpha=0.0 and alpha=1.0 are both valid."""
        GeomArea(alpha=0.0)
        GeomArea(alpha=1.0)

    def test_default_alpha_is_fractional(self) -> None:
        """Default alpha is 0.4 (semi-transparent)."""
        g = GeomArea()
        assert g.alpha == pytest.approx(0.4)
