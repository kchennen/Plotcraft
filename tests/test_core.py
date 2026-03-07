"""Integration tests for the PlotCraft fluent API."""

import polars as pl

import plotcraft as pc


class TestPlotCraftImmutability:
    """Verify that every PlotCraft method returns a new, independent instance."""

    def test_add_data_points_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """add_data_points() returns a new PlotCraft with one layer added."""
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.add_data_points()
        assert p1 is not p2
        assert len(p1._spec.layers) == 0
        assert len(p2._spec.layers) == 1

    def test_adjust_colors_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """adjust_colors() returns a new PlotCraft with a different color scheme."""
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.adjust_colors(["#FF0000", "#00FF00"])
        assert p1 is not p2
        assert p1._spec.color_scheme is not p2._spec.color_scheme

    def test_remove_legend_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """remove_legend() returns a new PlotCraft with legend_position set to 'none'."""
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.remove_legend()
        assert p1._spec.theme.legend_position == "right"
        assert p2._spec.theme.legend_position == "none"

    def test_chaining_preserves_independence(self, gene_response_df: pl.DataFrame) -> None:
        """Two chains from the same base do not share mutable state."""
        base = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points()
        plot_a = base.adjust_colors(["#FF0000"])
        plot_b = base.adjust_colors(["#0000FF"])
        assert plot_a._spec.color_scheme is not plot_b._spec.color_scheme


class TestPlotCraftAPI:
    """Verify the public PlotCraft method contracts."""

    def test_add_title(self, gene_response_df: pl.DataFrame) -> None:
        """add_title() stores the title string in the spec."""
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_title("Hello")
        assert p._spec.title == "Hello"

    def test_add_caption(self, gene_response_df: pl.DataFrame) -> None:
        """add_caption() stores the caption string in the spec."""
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_caption("n=24")
        assert p._spec.caption == "n=24"

    def test_repr(self, gene_response_df: pl.DataFrame) -> None:
        """__repr__ includes class name and layer count."""
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points().add_title("T")
        r = repr(p)
        assert "PlotCraft" in r
        assert "layers=1" in r

    def test_history_tracking(self, gene_response_df: pl.DataFrame) -> None:
        """Each method call appends its name to the spec history tuple."""
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points().add_title("T")
        assert "add_data_points" in p._spec.history
        assert "add_title" in p._spec.history
