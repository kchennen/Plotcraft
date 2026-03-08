"""Tests for GeomPoint rendering and validation."""

from __future__ import annotations

import matplotlib.pyplot as plt
import polars as pl
import pytest

from plotcraft.core.aes import Aes
from plotcraft.geoms.point import GeomPoint


class TestGeomPoint:
    """Test scatter plot geometry."""

    def test_draws_without_error(self) -> None:
        """GeomPoint.draw() completes without raising."""
        fig, ax = plt.subplots()
        data = pl.DataFrame({"x": [1.0, 2.0, 3.0], "y": [4.0, 5.0, 6.0]})
        geom = GeomPoint()
        geom.draw(ax, data, Aes(x="x", y="y"), {}, None)
        plt.close(fig)

    def test_draws_with_color(self) -> None:
        """GeomPoint handles discrete color grouping."""
        fig, ax = plt.subplots()
        data = pl.DataFrame(
            {
                "x": [1.0, 2.0, 1.0, 2.0],
                "y": [3.0, 4.0, 5.0, 6.0],
                "group": ["A", "A", "B", "B"],
            }
        )
        color_map = {"A": "#FF0000", "B": "#0000FF"}
        geom = GeomPoint()
        geom.draw(
            ax,
            data,
            Aes(x="x", y="y", color="group"),
            {"color_map": color_map},
            None,
        )
        plt.close(fig)


class TestGeomPointValidation:
    """GeomPoint rejects invalid constructor parameters."""

    def test_zero_size_raises(self) -> None:
        """size=0 raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            GeomPoint(size=0.0)

    def test_negative_size_raises(self) -> None:
        """Negative size raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            GeomPoint(size=-1.0)

    def test_alpha_above_one_raises(self) -> None:
        """Alpha > 1 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomPoint(alpha=1.1)

    def test_negative_alpha_raises(self) -> None:
        """Alpha < 0 raises ValueError."""
        with pytest.raises(ValueError, match="alpha"):
            GeomPoint(alpha=-0.1)

    def test_boundary_alpha_values_accepted(self) -> None:
        """alpha=0.0 and alpha=1.0 are both valid."""
        GeomPoint(alpha=0.0)
        GeomPoint(alpha=1.0)

    def test_positive_size_accepted(self) -> None:
        """Any positive size is accepted."""
        g = GeomPoint(size=0.001)
        assert g.size == pytest.approx(0.001)

    def test_default_marker_is_circle(self) -> None:
        """Default marker is 'o'."""
        g = GeomPoint()
        assert g.marker == "o"

    def test_custom_marker_accepted(self) -> None:
        """Custom markers (e.g. 's', '^') are accepted."""
        g = GeomPoint(marker="s")
        assert g.marker == "s"

    def test_show_colorbar_default_true(self) -> None:
        """show_colorbar defaults to True."""
        g = GeomPoint()
        assert g.show_colorbar is True

    def test_show_colorbar_can_be_disabled(self) -> None:
        """show_colorbar=False is accepted."""
        g = GeomPoint(show_colorbar=False)
        assert g.show_colorbar is False
