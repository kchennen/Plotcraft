"""Tests for GeomBar rendering."""

from __future__ import annotations

import matplotlib.pyplot as plt
import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.geoms.bar import GeomBar


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
