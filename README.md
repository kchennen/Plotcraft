<!-- markdownlint-disable MD013 MD033 MD041 -->
<div align="center">

<h1>Plotcraft</h1>

<p><em>Crafting publication-ready statistical graphics in Python.</em></p>

## Project Information

[![License](https://img.shields.io/github/license/kchennen/Plotcraft?style=flat-square&logo=opensourceinitiative)](LICENSE)
[![Python](https://img.shields.io/badge/python->=3.13-blue?style=flat-square&logo=python)](https://www.python.org/)

## We rely on

[![Matplotlib](https://img.shields.io/badge/Matplotlib-latest?style=flat-square&logo=python&color=11557C)](https://matplotlib.org/)
[![Polars](https://img.shields.io/badge/Polars-latest?style=flat-square&logo=polars&color=EDBB85)](https://pola-rs.github.io/polars-book/)

## Quality

[![CI](https://img.shields.io/github/actions/workflow/status/kchennen/Plotcraft/ci.yml?label=ci&style=flat-square&logo=github-actions)](https://github.com/kchennen/Plotcraft/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/kchennen/Plotcraft/graph/badge.svg?style=flat-square)](https://codecov.io/gh/kchennen/Plotcraft)
[![Mypy](https://img.shields.io/badge/mypy-strict-informational?style=flat-square&logo=python)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?style=flat-square&logo=python)](https://github.com/astral-sh/ruff)
[![GitHub issues](https://img.shields.io/github/issues/kchennen/Plotcraft?style=flat-square&logo=github)](https://github.com/kchennen/Plotcraft/issues)

[![Report a bug](https://img.shields.io/badge/🐛%20Report%20a%20bug-red?style=flat-square)](https://github.com/kchennen/Plotcraft/issues)
</div>
<!-- markdownlint-enable MD013 MD033 MD041 -->

---

Plotcraft is a Python data visualization library for building elegant, publication-ready statistical graphics from tidy
data. Inspired by the Grammar of Graphics and the [tidyplot](https://jbengler.github.io/tidyplots/) ecosystem, it
provides a clean, declarative, chainable API for constructing complex visualizations in a structured and intuitive way.

Plots are built **layer by layer** through a fluent method-chaining interface that cleanly separates data, aesthetic
mappings, and visual layers — making figures easy to create, reproduce, and customize for scientific publications.

---

## Features

- 🔗 **Fluent API** — every method returns a new `PlotCraft` instance (immutable copy pattern), enabling safe chaining
- 📊 **Multiple chart types** — scatter, bar, line, area, dot, and dash geometries
- 🎨 **Rich color system** — 40+ built-in palettes across journal, discrete, continuous, and diverging categories;
  palette modifiers (saturation, reverse, custom)
- 🔢 **Continuous color scales** — scatter plots mapped to numeric columns with automatic colorbars
- 📦 **Bundled datasets** — 11 ready-to-use example datasets for quick prototyping
- 📐 **Size control** — figure dimensions in mm, cm, or inches
- 💾 **Export** — save to PNG, PDF, SVG, or any matplotlib-supported format
- ✅ **Type-safe** — fully typed, passes `mypy --strict`

---

## Installation

```bash
# Using uv (recommended)
uv add plotcraft

# Using pip
pip install plotcraft
```

### Optional extras

```bash
uv add "plotcraft[pandas]"   # pandas DataFrame support
uv add "plotcraft[bio]"      # scipy-based statistical layers (coming soon)
```

---

## Quick Start

```python
import plotcraft as pc

# Load a built-in dataset
df = pc.load_dataset("study")

# Build a plot with method chaining
(
    pc.plotcraft(df, x="group", color="treatment")
    .add_count_bar()
    .add_title("Participant Count by Group")
    .adjust_colors(pc.colors_journal_npg)
    .adjust_size(width=120, height=90, units="mm")
    .save_plot("figure1.png")
)
```

```python
# Scatter plot with continuous color scale
df = pc.load_dataset("gene_expression")

fig, ax = (
    pc.plotcraft(df, x="timepoint", y="expression", color="log2fc")
    .add_data_points(size=3)
    .adjust_colors(pc.colors_continuous_viridis)
    .add_title("Gene Expression Over Time")
    .render()
)
```

---

## Development

```bash
git clone https://github.com/kchennen/Plotcraft.git
cd Plotcraft

uv sync --all-groups      # install all dependencies

uv run pytest             # run tests
uv run mypy src/plotcraft # type check
uv run ruff check src/    # lint
uv run ruff format src/   # format
```

### Project structure

```text
src/plotcraft/
├── core/          # PlotCraft API, PlotSpec, Aes, Layer
├── geoms/         # Geometry classes (GeomPoint, GeomBar, GeomLine, …)
├── stats/         # Statistical transforms (StatIdentity, StatCount)
├── positions/     # Position adjustments
├── colors/        # Color palettes and ColorScheme
├── render/        # RenderEngine (matplotlib backend)
└── datasets/      # Bundled example datasets
```

---

## Roadmap

- [x] Fluent chainable API
- [x] Scatter / point geometry
- [x] Bar, line, area, dot, dash count geometries
- [x] Discrete and journal color palettes
- [x] Continuous color scales with colorbar
- [x] Diverging color scales
- [x] Palette modifiers (saturation, reverse, custom)
- [x] Bundled datasets
- [ ] Statistical layers (mean, median, error bars, regression)
- [ ] Box plots and violin plots
- [ ] Faceting (small multiples)
- [ ] PyPI release

---

Built with ❤️ for your pleasure and our leisure by the 🦡 **Blaireau Company**
