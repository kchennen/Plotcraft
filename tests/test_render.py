"""Tests for the rendering pipeline."""

import os
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import plotcraft as pc
from plotcraft.colors.continuous import colors_continuous_viridis
from plotcraft.colors.journal import colors_journal_npg
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
        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
        plt.close(fig)

    def test_render_with_color_produces_legend(self, scatter_spec: PlotSpec):
        """Color aesthetic generates legend entries for each group."""
        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        _handles, labels = ax.get_legend_handles_labels()
        assert set(labels) == {"control", "treated"}
        plt.close(fig)

    def test_categorical_xaxis_tick_positions(self, scatter_spec: PlotSpec):
        """Categorical x column maps to contiguous integer tick positions."""
        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        # Polars .unique().sort() gives alphabetical order:
        # BRCA1 → 0, EGFR → 1, TP53 → 2
        assert list(ax.get_xticks()) == [0, 1, 2]
        plt.close(fig)

    def test_categorical_xaxis_tick_labels(self, scatter_spec: PlotSpec):
        """Categorical x-axis labels match the sorted unique category values."""
        engine = RenderEngine()
        fig, ax = engine.render(scatter_spec)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["BRCA1", "EGFR", "TP53"]
        plt.close(fig)

    def test_categorical_xaxis_horizontal_margin(self, scatter_spec: PlotSpec):
        """Categorical x-axis applies 0.15 horizontal margin for breathing room."""
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


class TestContinuousColor:
    """Test continuous color mapping in the render pipeline."""

    def test_continuous_scatter(self) -> None:
        """Scatter with continuous color palette renders without error."""
        df = pl.DataFrame(
            {
                "x": [1.0, 2.0, 3.0, 4.0, 5.0],
                "y": [2.0, 4.0, 1.0, 5.0, 3.0],
                "value": [0.0, 0.25, 0.5, 0.75, 1.0],
            }
        )
        fig, _ = (
            pc.plotcraft(df, x="x", y="y", color="value")
            .add_data_points()
            .adjust_colors(colors_continuous_viridis)
            .render()
        )
        plt.close(fig)


class TestFullWorkflow:
    """End-to-end workflow tests combining Sprint 1 + Sprint 2 features."""

    def test_definition_of_done(self, tmp_path: Path) -> None:
        """The Sprint 2 Definition of Done chain succeeds."""
        df = pc.load_dataset("study")
        out = str(tmp_path / "test_output.png")
        (
            pc.plotcraft(df, x="group", color="treatment")
            .add_count_bar()
            .add_title("Participant Count")
            .adjust_colors(colors_journal_npg)
            .remove_legend()
            .save_plot(out)
        )
        assert (tmp_path / "test_output.png").exists()

    def test_saturation_workflow(self) -> None:
        """with_saturation() integrates with the render pipeline."""
        df = pc.load_dataset("study")
        faded = colors_journal_npg.with_saturation(0.3)
        fig, _ = pc.plotcraft(df, x="group", color="treatment").add_count_bar().adjust_colors(faded).render()
        plt.close(fig)

    def test_reversed_workflow(self) -> None:
        """reversed() integrates with the render pipeline."""
        df = pc.load_dataset("study")
        rev = colors_journal_npg.reversed()
        fig, _ = pc.plotcraft(df, x="group", color="treatment").add_count_bar().adjust_colors(rev).render()
        plt.close(fig)

    def test_new_color_scheme(self) -> None:
        """new_color_scheme() creates usable palettes."""
        df = pc.load_dataset("study")
        custom = pc.new_color_scheme("test", ["#FF0000", "#00FF00", "#0000FF"])
        fig, _ = pc.plotcraft(df, x="group", color="treatment").add_count_bar().adjust_colors(custom).render()
        plt.close(fig)
