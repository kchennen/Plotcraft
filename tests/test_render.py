"""Tests for the rendering pipeline."""

import os
import tempfile

import polars as pl
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import plotcraft as pc
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
        margins = ax.margins()
        assert margins is not None, "ax.margins() returned None"
        x_margin = float(margins[0])  # float() resolves the Unknown stub type
        assert x_margin == pytest.approx(0.15)
        plt.close(fig)


class TestSavePlot:
    """Tests for PlotCraft.save_plot() file output."""

    def test_save_png(self, gene_response_df: pl.DataFrame) -> None:
        """save_plot() writes a non-empty PNG file and returns self for chaining."""
        p = (
            pc.plotcraft(gene_response_df, x="gene", y="expression", color="treatment")
            .add_data_points()
            .add_title("Test Figure")
        )
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = p.save_plot(path)
            assert result is p  # save_plot returns self
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_save_pdf(self, gene_response_df: pl.DataFrame) -> None:
        """save_plot() writes a non-empty PDF file."""
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            p.save_plot(path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)


class TestFullWorkflow:
    """Tests for a complete PlotCraft workflow from spec construction to file output."""

    def test_definition_of_done(self, gene_response_df: pl.DataFrame) -> None:
        """The exact chain from the Sprint 1 Definition of Done."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            (
                pc.plotcraft(gene_response_df, x="gene", y="expression", color="treatment")
                .add_data_points()
                .add_title("Gene Response")
                .adjust_colors(["#E41A1C", "#377EB8"])
                .remove_legend()
                .save_plot(path)
            )
            assert os.path.exists(path)
            assert os.path.getsize(path) > 1000  # Non-trivial file
        finally:
            os.unlink(path)

    def test_branching_workflow(self, gene_response_df: pl.DataFrame) -> None:
        """Verify branching produces independent plots."""
        base = pc.plotcraft(gene_response_df, x="gene", y="expression", color="treatment").add_data_points()
        plot_a = base.adjust_colors(["#FF0000", "#00FF00"])
        plot_b = base.adjust_colors(["#0000FF", "#FFFF00"])

        with (
            tempfile.NamedTemporaryFile(suffix=".png", delete=False) as fa,
            tempfile.NamedTemporaryFile(suffix=".png", delete=False) as fb,
        ):
            try:
                plot_a.save_plot(fa.name)
                plot_b.save_plot(fb.name)
                assert os.path.getsize(fa.name) > 0
                assert os.path.getsize(fb.name) > 0
            finally:
                os.unlink(fa.name)
                os.unlink(fb.name)
