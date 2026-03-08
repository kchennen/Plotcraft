"""Integration tests for the PlotCraft fluent API."""

import matplotlib.pyplot as plt
import polars as pl

import plotcraft as pc


class TestPlotCraftImmutability:
    """Verify that every PlotCraft method returns a new, independent instance."""

    def test_add_data_points_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """Test that add_data_points() returns a new PlotCraft instance with an added layer.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.add_data_points()
        assert p1 is not p2
        assert len(p1.spec.layers) == 0
        assert len(p2.spec.layers) == 1

    def test_adjust_colors_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """Test that adjust_colors() returns a new PlotCraft instance with a different color scheme.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.adjust_colors(["#FF0000", "#00FF00"])
        assert p1 is not p2
        assert p1.spec.color_scheme is not p2.spec.color_scheme

    def test_remove_legend_returns_new_instance(self, gene_response_df: pl.DataFrame) -> None:
        """Test that remove_legend() returns a new PlotCraft instance with legend_position set to 'none'.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p1 = pc.plotcraft(gene_response_df, x="gene", y="expression")
        p2 = p1.remove_legend()
        assert p1.spec.theme.legend_position == "right"
        assert p2.spec.theme.legend_position == "none"

    def test_chaining_preserves_independence(self, gene_response_df: pl.DataFrame) -> None:
        """Test that two chains from the same base do not share mutable state.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        base = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points()
        plot_a = base.adjust_colors(["#FF0000"])
        plot_b = base.adjust_colors(["#0000FF"])
        assert plot_a.spec.color_scheme is not plot_b.spec.color_scheme


class TestPlotCraftAPI:
    """Verify the public PlotCraft method contracts."""

    def test_add_title(self, gene_response_df: pl.DataFrame) -> None:
        """Test that add_title() stores the title string in the spec.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_title("Hello")
        assert p.spec.title == "Hello"

    def test_add_caption(self, gene_response_df: pl.DataFrame) -> None:
        """Test that add_caption() stores the caption string in the spec.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_caption("n=24")
        assert p.spec.caption == "n=24"

    def test_repr(self, gene_response_df: pl.DataFrame) -> None:
        """Test that __repr__ includes class name and layer count.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points().add_title("T")
        r = repr(p)
        assert "PlotCraft" in r
        assert "layers=1" in r

    def test_history_tracking(self, gene_response_df: pl.DataFrame) -> None:
        """Test that each method call appends its name to the spec history tuple.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").add_data_points().add_title("T")
        assert "add_data_points" in p.spec.history
        assert "add_title" in p.spec.history


class TestPlotCraftStyling:
    """Verify size and axis-title adjust/remove methods."""

    def test_adjust_size_mm(self, gene_response_df: pl.DataFrame) -> None:
        """Test that adjust_size() stores width and height in millimetres when units='mm'.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").adjust_size(width=100, height=60)
        assert p.spec.width_mm == 100.0
        assert p.spec.height_mm == 60.0

    def test_adjust_size_inches(self, gene_response_df: pl.DataFrame) -> None:
        """Test that adjust_size() converts inches to mm (1 in = 25.4 mm).

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").adjust_size(width=3.0, units="in")
        assert abs(p.spec.width_mm - 76.2) < 0.01

    def test_remove_axis_titles(self, gene_response_df: pl.DataFrame) -> None:
        """Test that remove_x/y_axis_title() sets the corresponding title to an empty string.

        Args:
            gene_response_df: A fixture providing a sample DataFrame for testing.
        """
        p = pc.plotcraft(gene_response_df, x="gene", y="expression").remove_x_axis_title().remove_y_axis_title()
        assert p.spec.x_title == ""
        assert p.spec.y_title == ""


class TestCountMethods:
    """Integration tests for add_count_* methods."""

    def test_add_count_bar(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_bar produces a renderable plot.

        Args:
            sample_df: A fixture providing a sample DataFrame for testing.
        """
        import plotcraft as pc

        plot = pc.plotcraft(sample_df, x="group", color="treatment")
        result = plot.add_count_bar()
        assert "add_count_bar" in result.spec.history
        # Should not raise
        fig, _ = result.render()
        plt.close(fig)

    def test_add_count_dot(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_dot produces a renderable plot.

        Args:
            sample_df: A fixture providing a sample DataFrame for testing.
        """
        import plotcraft as pc

        fig, _ = pc.plotcraft(sample_df, x="group").add_count_dot().render()
        plt.close(fig)

    def test_add_count_dash(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_dash produces a renderable plot.

        Args:
            sample_df: A fixture providing a sample DataFrame for testing.
        """
        import plotcraft as pc

        fig, _ = pc.plotcraft(sample_df, x="group").add_count_dash().render()
        plt.close(fig)

    def test_add_count_line(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_line produces a renderable plot.

        Args:
            sample_df (pl.DataFrame): _description_
        """
        import plotcraft as pc

        fig, _ = pc.plotcraft(sample_df, x="group").add_count_line().render()
        plt.close(fig)

    def test_add_count_area(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_area produces a renderable plot.

        Args:
            sample_df: A fixture providing a sample DataFrame for testing.
        """
        import plotcraft as pc

        fig, _ = pc.plotcraft(sample_df, x="group").add_count_area().render()
        plt.close(fig)

    def test_count_bar_with_colors(self, sample_df: pl.DataFrame) -> None:
        """Test that add_count_bar produces a renderable plot with color grouping.

        Args:
            sample_df (pl.DataFrame): _description_
        """
        import plotcraft as pc

        fig, _ = (
            pc.plotcraft(sample_df, x="group", color="treatment")
            .add_count_bar()
            .adjust_colors(pc.colors_journal_npg)
            .render()
        )
        plt.close(fig)
