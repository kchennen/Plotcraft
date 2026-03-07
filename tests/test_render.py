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
