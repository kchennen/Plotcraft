"""Tests for the rendering pipeline."""

import polars as pl
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from plotcraft.core.aes import Aes
from plotcraft.core.layer import Layer
from plotcraft.core.spec import PlotSpec
from plotcraft.geoms.point import GeomPoint
from plotcraft.positions.identity import PositionIdentity
from plotcraft.render.engine import RenderEngine
from plotcraft.stats.identity import StatIdentity


@pytest.fixture
def scatter_spec(gene_response_df: pl.DataFrame) -> PlotSpec:
    """A PlotSpec with one scatter layer, built manually.

    Args:
        gene_response_df: The shared test DataFrame fixture.

    Returns:
        A PlotSpec configured with a single GeomPoint layer.
    """
    layer = Layer(
        geom=GeomPoint(size=3.0),
        stat=StatIdentity(),
        position=PositionIdentity(),
    )
    return PlotSpec(
        data=gene_response_df,
        aes=Aes(x="gene", y="expression", color="treatment"),
        layers=(layer,),
        title="Gene Response",
    )


class TestRenderEngine:
    """Tests for RenderEngine.render()."""

    def test_render_returns_figure_and_axes(self, scatter_spec: PlotSpec):
        """Render produces a matplotlib Figure and Axes."""
        import matplotlib.pyplot as plt

        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
        plt.close(fig)

    def test_render_with_color_produces_legend(self, scatter_spec: PlotSpec):
        """Color aesthetic generates legend entries for each group."""
        import matplotlib.pyplot as plt

        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        _handles, labels = ax.get_legend_handles_labels()
        assert set(labels) == {"control", "treated"}
        plt.close(fig)

    def test_categorical_xaxis_tick_positions(self, scatter_spec: PlotSpec):
        """Categorical x column maps to contiguous integer tick positions."""
        import matplotlib.pyplot as plt

        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        # Polars .unique().sort() gives alphabetical order:
        # BRCA1 → 0, EGFR → 1, TP53 → 2
        assert list(ax.get_xticks()) == [0, 1, 2]
        plt.close(fig)

    def test_categorical_xaxis_tick_labels(self, scatter_spec: PlotSpec):
        """Categorical x-axis labels match the sorted unique category values."""
        import matplotlib.pyplot as plt

        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["BRCA1", "EGFR", "TP53"]
        plt.close(fig)

    def test_categorical_xaxis_horizontal_margin(self, scatter_spec: PlotSpec):
        """Categorical x-axis applies 0.15 horizontal margin for breathing room."""
        import matplotlib.pyplot as plt
        import pytest

        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        x_margin, _ = ax.margins()
        assert x_margin == pytest.approx(0.15)
        plt.close(fig)
