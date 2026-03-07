"""Tests for PlotSpec immutability."""

from dataclasses import replace

import polars as pl

from plotcraft.core.aes import Aes
from plotcraft.core.spec import PlotSpec


def test_plotspec_is_frozen():
    """Assigning to a frozen PlotSpec raises AttributeError."""
    spec = PlotSpec(data=pl.DataFrame({"x": [1]}), aes=Aes(x="x"))
    try:
        spec.title = "new"  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"
    except AttributeError:
        pass


def test_plotspec_replace_creates_new_instance():
    """dataclasses.replace returns a new spec without mutating the original."""
    spec = PlotSpec(data=pl.DataFrame({"x": [1]}), aes=Aes(x="x"))
    new_spec = replace(spec, title="Hello")
    assert new_spec.title == "Hello"
    assert spec.title == ""  # original unchanged


def test_plotspec_layers_are_tuples():
    """Layers default to an empty tuple for immutability."""
    spec = PlotSpec(data=pl.DataFrame({"x": [1]}), aes=Aes(x="x"))
    assert isinstance(spec.layers, tuple)
