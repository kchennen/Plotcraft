"""Tests for GeomBar and GeomDash rendering and validation."""

from __future__ import annotations

import matplotlib.pyplot as plt
import polars as pl
import pytest

from plotcraft.core.aes import Aes
from plotcraft.geoms.bar import GeomBar, GeomDash


class TestGeomBar:
    """Test bar chart geometry."""

    def test_draws_without_error(self) -> None:
        """GeomBar.draw() completes without raising."""
        fig, ax = plt.subplots()
        data = pl.DataFrame(
            {
                "group": ["A", "B", "C"],
                "_count": [5, 3, 7],
            }
        )
        geom = GeomBar()
        geom.draw(ax, data, Aes(x="group", y="_count"), {}, None)
        plt.close(fig)

    def test_draws_with_color(self) -> None:
        """GeomBar handles color grouping."""
        fig, ax = plt.subplots()
        data = pl.DataFrame(
            {
                "group": ["A", "A", "B", "B"],
                "treatment": ["ctrl", "drug", "ctrl", "drug"],
                "_count": [5, 3, 7, 4],
            }
        )
        color_map = {"ctrl": "#FF0000", "drug": "#0000FF"}
        x_cat_map = {"A": 0, "B": 1}
        geom = GeomBar()
        geom.draw(
            ax,
            data,
            Aes(x="group", y="_count", color="treatment"),
            {"color_map": color_map, "x_cat_map": x_cat_map},
            None,
        )
        plt.close(fig)


class TestGeomBarValidation:
    """GeomBar rejects invalid constructor parameters."""

    def test_zero_width_raises(self) -> None:
        """width=0 raises ValueError."""
        with pytest.raises(ValueError, match="width"):
            GeomBar(width=0.0)

    def test_negative_width_raises(self) -> None:
        """Negative width raises ValueError."""
        with pytest.raises(ValueError, match="width"):
            GeomBar(width=-0.5)

    def test_alpha_above_one_raises(self) -> None:
        """Alpha > 1 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomBar(alpha=1.1)

    def test_negative_alpha_raises(self) -> None:
        """Alpha < 0 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomBar(alpha=-0.1)

    def test_boundary_alpha_values_accepted(self) -> None:
        """alpha=0.0 and alpha=1.0 are both valid."""
        GeomBar(alpha=0.0)
        GeomBar(alpha=1.0)

    def test_positive_width_accepted(self) -> None:
        """Any positive width is accepted."""
        g = GeomBar(width=0.001)
        assert g.width == pytest.approx(0.001)


class TestGeomDashValidation:
    """GeomDash rejects invalid constructor parameters."""

    def test_zero_linewidth_raises(self) -> None:
        """linewidth=0 raises ValueError."""
        with pytest.raises(ValueError, match="linewidth"):
            GeomDash(linewidth=0.0)

    def test_negative_linewidth_raises(self) -> None:
        """Negative linewidth raises ValueError."""
        with pytest.raises(ValueError, match="linewidth"):
            GeomDash(linewidth=-1.0)

    def test_positive_linewidth_accepted(self) -> None:
        """Any positive linewidth is accepted."""
        g = GeomDash(linewidth=0.1)
        assert g.linewidth == pytest.approx(0.1)
