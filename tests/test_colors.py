"""Tests for the color system — ColorScheme, utilities, and palettes."""

from __future__ import annotations

import re

import pytest

from plotcraft.colors import continuous, discrete, diverging, journal
from plotcraft.colors.discrete import colors_discrete_friendly
from plotcraft.colors.palettes import ColorScheme, new_color_scheme
from plotcraft.colors.utils import apply_saturation, interpolate_colors

# Parametrized palette inventory — ensures every palette is importable
# and has the correct family/type.
_DISCRETE_PALETTES = [
    (discrete.colors_discrete_friendly, "friendly", 7),
    (discrete.colors_discrete_friendly_long, "friendly_long", 15),
    (discrete.colors_discrete_seaside, "seaside", 7),
    (discrete.colors_discrete_apple, "apple", 9),
    (discrete.colors_discrete_ibm, "ibm", 5),
    (discrete.colors_discrete_candy, "candy", 7),
    (discrete.colors_discrete_alger, "alger", 5),
    (discrete.colors_discrete_metro, "metro", 5),
    (discrete.colors_discrete_okabeito, "okabeito", 8),
    (discrete.colors_discrete_rainbow, "rainbow", 8),
    (discrete.colors_discrete_wong, "wong", 8),
    (discrete.colors_discrete_tableau10, "tableau10", 10),
    (discrete.colors_discrete_tol_vibrant, "tol_vibrant", 7),
    (discrete.colors_discrete_tol_muted, "tol_muted", 9),
    (discrete.colors_discrete_tol_light, "tol_light", 9),
]

_JOURNAL_PALETTES = [
    (journal.colors_journal_npg, "npg", 10),
    (journal.colors_journal_lancet, "lancet", 8),
    (journal.colors_journal_nejm, "nejm", 8),
    (journal.colors_journal_jama, "jama", 7),
    (journal.colors_journal_aaas, "aaas", 10),
    (journal.colors_journal_d3, "d3", 10),
    (journal.colors_journal_igv, "igv", 10),
]

_CONTINUOUS_PALETTES = [
    (continuous.colors_continuous_viridis, "viridis"),
    (continuous.colors_continuous_magma, "magma"),
    (continuous.colors_continuous_inferno, "inferno"),
    (continuous.colors_continuous_plasma, "plasma"),
    (continuous.colors_continuous_cividis, "cividis"),
    (continuous.colors_continuous_rocket, "rocket"),
    (continuous.colors_continuous_mako, "mako"),
    (continuous.colors_continuous_turbo, "turbo"),
    (continuous.colors_continuous_bluepinkyellow, "bluepinkyellow"),
]

_DIVERGING_PALETTES = [
    (diverging.colors_diverging_blue2red, "blue2red"),
    (diverging.colors_diverging_blue2brown, "blue2brown"),
    (diverging.colors_diverging_spectral, "spectral"),
    (diverging.colors_diverging_icefire, "icefire"),
    (diverging.colors_diverging_BuRd, "BuRd"),
    (diverging.colors_diverging_BuYlRd, "BuYlRd"),
]


class TestInterpolateColors:
    """Test the interpolation utility."""

    def test_returns_exact_n(self) -> None:
        """interpolate_colors() always returns exactly n colors."""
        colors = ("#FF0000", "#00FF00", "#0000FF")
        result = interpolate_colors(colors, 5)
        assert len(result) == 5

    def test_all_hex(self) -> None:
        """All returned values are valid 6-digit hex color strings."""
        colors = ("#FF0000", "#0000FF")
        result = interpolate_colors(colors, 10)
        for c in result:
            assert re.match(r"^#[0-9a-fA-F]{6}$", c), f"Not a hex color: {c}"

    def test_endpoints_preserved(self) -> None:
        """The first and last input colors are preserved as-is at the endpoints."""
        colors = ("#FF0000", "#0000FF")
        result = interpolate_colors(colors, 3)
        assert result[0].lower() == "#ff0000"
        assert result[-1].lower() == "#0000ff"

    def test_zero_returns_empty(self) -> None:
        """Requesting n=0 colors returns an empty list."""
        assert interpolate_colors(("#FF0000",), 0) == []

    def test_one_returns_first(self) -> None:
        """Requesting n=1 returns only the first anchor color."""
        result = interpolate_colors(("#FF0000", "#0000FF"), 1)
        assert len(result) == 1
        assert result[0].lower() == "#ff0000"


class TestApplySaturation:
    """Test saturation adjustment."""

    def test_identity(self) -> None:
        """Saturation=1.0 should return approximately the same color."""
        original = "#E64B35"
        result = apply_saturation(original, 1.0)
        assert result.lower() == original.lower()

    def test_desaturate(self) -> None:
        """Saturation=0.0 should produce a grey (R=G=B)."""
        result = apply_saturation("#E64B35", 0.0)
        # Parse the hex and check that it's a grey (R=G=B approximately)
        import matplotlib.colors as mcolors

        r, g, b = mcolors.to_rgb(result)
        assert abs(r - g) < 0.02
        assert abs(g - b) < 0.02


class TestColorSchemeGetColors:
    """Test the enhanced get_colors method."""

    def test_subsample_discrete(self) -> None:
        """When n <= base count for discrete, subsample."""
        scheme = ColorScheme(name="test", colors=("#A", "#B", "#C", "#D", "#E"))
        result = scheme.get_colors(3)
        assert result == ["#A", "#B", "#C"]

    def test_interpolate_when_exceeds(self) -> None:
        """When n > base count for discrete, interpolate."""
        result = colors_discrete_friendly.get_colors(20)
        assert len(result) == 20
        for c in result:
            assert c.startswith("#")

    def test_continuous_always_interpolates(self) -> None:
        """Continuous palettes always interpolate, even for small n."""
        scheme = ColorScheme(
            name="test_cont",
            colors=("#FF0000", "#FFFF00", "#00FF00"),
            palette_type="continuous",
        )
        # With n=2, a discrete palette would subsample but continuous interpolates
        result = scheme.get_colors(2)
        assert len(result) == 2
        # Endpoints should match the anchors
        assert result[0].lower() == "#ff0000"
        assert result[-1].lower() == "#00ff00"

    def test_empty_for_zero(self) -> None:
        """Requesting n=0 colors returns an empty list."""
        assert colors_discrete_friendly.get_colors(0) == []


class TestColorSchemeWithSaturation:
    """Test with_saturation()."""

    def test_returns_new_instance(self) -> None:
        """with_saturation() returns a new ColorScheme, not the original, with a _sN.N suffix."""
        original = colors_discrete_friendly
        adjusted = original.with_saturation(0.5)
        assert adjusted is not original
        assert adjusted.name == "friendly_s0.5"

    def test_preserves_count(self) -> None:
        """The adjusted scheme contains the same number of colors as the original."""
        adjusted = colors_discrete_friendly.with_saturation(0.5)
        assert len(adjusted.colors) == len(colors_discrete_friendly.colors)

    def test_colors_differ(self) -> None:
        """Colors in the adjusted scheme differ from the originals when saturation changes."""
        adjusted = colors_discrete_friendly.with_saturation(0.3)
        assert adjusted.colors != colors_discrete_friendly.colors


class TestColorSchemeReversed:
    """Test reversed()."""

    def test_reversed_order(self) -> None:
        """reversed() returns a new scheme with colors in reverse order and a _r name suffix."""
        scheme = ColorScheme(name="abc", colors=("#A", "#B", "#C"))
        rev = scheme.reversed()
        assert rev.colors == ("#C", "#B", "#A")
        assert rev.name == "abc_r"

    def test_double_reverse(self) -> None:
        """Reversing a scheme twice restores the original color order."""
        original = colors_discrete_friendly
        double = original.reversed().reversed()
        assert double.colors == original.colors


class TestNewColorScheme:
    """Test the factory function."""

    def test_creates_discrete(self) -> None:
        """new_color_scheme() creates a discrete ColorScheme with the given name and colors."""
        s = new_color_scheme("mine", ["#FF0000", "#00FF00"])
        assert s.name == "mine"
        assert s.palette_type == "discrete"
        assert len(s.colors) == 2

    def test_creates_continuous(self) -> None:
        """new_color_scheme() respects an explicit palette_type argument."""
        s = new_color_scheme("grad", ["#000", "#FFF"], palette_type="continuous")
        assert s.palette_type == "continuous"


class TestPaletteInventory:
    """Verify every palette is importable with correct metadata."""

    @pytest.mark.parametrize("scheme,name,count", _DISCRETE_PALETTES)
    def test_discrete_palette(self, scheme: ColorScheme, name: str, count: int) -> None:
        """Each discrete palette has the correct name, type, and exact color count."""
        assert scheme.name == name
        assert scheme.palette_type == "discrete"
        assert len(scheme.colors) == count

    @pytest.mark.parametrize("scheme,name,count", _JOURNAL_PALETTES)
    def test_journal_palette(self, scheme: ColorScheme, name: str, count: int) -> None:
        """Each journal palette is typed as discrete and has the correct name and color count."""
        assert scheme.name == name
        assert scheme.palette_type == "discrete"
        assert len(scheme.colors) == count

    @pytest.mark.parametrize("scheme,name", _CONTINUOUS_PALETTES)
    def test_continuous_palette(self, scheme: ColorScheme, name: str) -> None:
        """Each continuous palette has the correct name, type, and at least 3 anchor colors."""
        assert scheme.name == name
        assert scheme.palette_type == "continuous"
        assert len(scheme.colors) >= 3  # Need at least 3 anchors for smooth gradients

    @pytest.mark.parametrize("scheme,name", _DIVERGING_PALETTES)
    def test_diverging_palette(self, scheme: ColorScheme, name: str) -> None:
        """Each diverging palette has the correct name, type, and at least 5 anchor colors."""
        assert scheme.name == name
        assert scheme.palette_type == "diverging"
        assert len(scheme.colors) >= 5  # Diverging needs both wings + midpoint


class TestPaletteTotals:
    """Quick sanity check — we promised 37 palettes total."""

    def test_total_count(self) -> None:
        """The palette inventory totals exactly 37: 15 discrete + 7 journal + 9 continuous + 6 diverging."""
        assert len(_DISCRETE_PALETTES) == 15
        assert len(_JOURNAL_PALETTES) == 7
        assert len(_CONTINUOUS_PALETTES) == 9
        assert len(_DIVERGING_PALETTES) == 6
        total = 15 + 7 + 9 + 6
        assert total == 37
