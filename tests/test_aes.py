"""Tests for the Aes dataclass."""

from plotcraft.core.aes import Aes


class TestAesMerge:
    """Tests for Aes.merge()."""

    def test_merge_adds_fields(self):
        """Merging fills in None fields from the other Aes."""
        a = Aes(x="a")
        b = Aes(y="b")
        merged = a.merge(b)
        assert merged.x == "a"
        assert merged.y == "b"

    def test_merge_overrides(self):
        """Non-None fields in other take precedence."""
        a = Aes(x="a")
        b = Aes(x="b")
        assert a.merge(b).x == "b"

    def test_merge_does_not_mutate_original(self):
        """Merge returns a new Aes; the original is unchanged."""
        a = Aes(x="a")
        b = Aes(x="b")
        a.merge(b)
        assert a.x == "a"

    def test_merge_empty_is_identity(self):
        """Merging with an empty Aes returns an equal copy."""
        a = Aes(x="a", y="b", color="c")
        assert a.merge(Aes()) == a


class TestAesResolveFill:
    """Tests for Aes.resolve_fill()."""

    def test_fill_defaults_to_color(self):
        """Fill is set to color when fill is None."""
        a = Aes(color="c")
        resolved = a.resolve_fill()
        assert resolved.fill == "c"
        assert resolved.color == "c"

    def test_explicit_fill_not_overridden(self):
        """An explicit fill is preserved even when color is set."""
        a = Aes(color="c", fill="f")
        assert a.resolve_fill().fill == "f"

    def test_no_color_no_fill(self):
        """Without color or fill, resolve_fill is a no-op."""
        a = Aes(x="a")
        assert a.resolve_fill() == a
