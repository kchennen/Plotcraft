# Plotcraft

> Crafting publication-ready statistical graphics in Python.

[![CI][ci-badge]][ci-url]
[![Coverage][cov-badge]][cov-url]
[![Python 3.13+][py-badge]][py-url]
[![License: Apache 2.0][lic-badge]][lic-url]
[![Ruff][ruff-badge]][ruff-url]
[![Mypy: strict][mypy-badge]][mypy-url]

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

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

---

<!-- markdownlint-disable MD013 -->
[ci-badge]: https://github.com/kchennen/Plotcraft/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/kchennen/Plotcraft/actions/workflows/ci.yml
[cov-badge]: https://codecov.io/gh/kchennen/Plotcraft/graph/badge.svg
[cov-url]: https://codecov.io/gh/kchennen/Plotcraft
[py-badge]: https://img.shields.io/badge/python-3.13%2B-blue.svg
[py-url]: https://www.python.org/downloads/
[lic-badge]: https://img.shields.io/badge/license-Apache--2.0-green.svg
[lic-url]: https://github.com/kchennen/Plotcraft/blob/main/LICENSE
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff-url]: https://github.com/astral-sh/ruff
[mypy-badge]: https://img.shields.io/badge/mypy-strict-blue.svg
[mypy-url]: https://mypy-lang.org/
<!-- markdownlint-enable MD013 -->
