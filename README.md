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

## API Overview

### Entry point

```python
pc.plotcraft(data, x=..., y=..., color=..., fill=...)
```

### Chart layers

| Method | Description |
|---|---|
| `.add_data_points(size, alpha)` | Scatter plot of individual data points |
| `.add_count_bar(width, alpha)` | Vertical bars showing counts per group |
| `.add_count_line(linewidth)` | Connected lines showing counts per group |
| `.add_count_area(alpha)` | Filled area showing counts per group |
| `.add_count_dot(size)` | Dots at count values per group |
| `.add_count_dash(linewidth)` | Horizontal dashes at count values per group |

### Annotations & adjustments

| Method | Description |
|---|---|
| `.add_title(title)` | Set the plot title |
| `.add_caption(caption)` | Add a caption below the plot |
| `.adjust_colors(palette)` | Apply a color palette (ColorScheme, list, or dict) |
| `.adjust_size(width, height, units)` | Set figure dimensions (`"mm"`, `"cm"`, `"in"`) |
| `.remove_legend()` | Hide the legend |
| `.remove_x_axis_title()` | Remove the x-axis label |
| `.remove_y_axis_title()` | Remove the y-axis label |

### Terminal methods

| Method | Returns | Description |
|---|---|---|
| `.render()` | `(Figure, Axes)` | Render and return matplotlib objects |
| `.save_plot(path, dpi=300)` | `PlotCraft` | Save to file (chainable) |
| `.view_plot()` | `PlotCraft` | Display interactively (chainable) |

---

## Color Palettes

Plotcraft ships with 40+ palettes in four categories.

### Journal palettes

Designed to match the color schemes of major scientific journals.

```python
pc.colors_journal_npg    # Nature Publishing Group
pc.colors_journal_aaas   # Science / AAAS
pc.colors_journal_jama   # JAMA
pc.colors_journal_lancet # The Lancet
pc.colors_journal_nejm   # New England Journal of Medicine
pc.colors_journal_d3     # D3.js category10
pc.colors_journal_igv    # IGV genome browser
```

### Discrete palettes

Colorblind-friendly and general-purpose categorical palettes.

```python
pc.colors_discrete_okabeito      # Okabe & Ito (colorblind-safe)
pc.colors_discrete_wong          # Wong (colorblind-safe)
pc.colors_discrete_ibm           # IBM Design (colorblind-safe)
pc.colors_discrete_tableau10     # Tableau 10
pc.colors_discrete_tol_vibrant   # Paul Tol vibrant
pc.colors_discrete_tol_muted     # Paul Tol muted
# ... and more
```

### Continuous palettes

For mapping numeric values to color gradients.

```python
pc.colors_continuous_viridis
pc.colors_continuous_plasma
pc.colors_continuous_magma
pc.colors_continuous_inferno
pc.colors_continuous_cividis
# ... and more
```

### Diverging palettes

For data that diverges around a meaningful midpoint.

```python
pc.colors_diverging_blue2red
pc.colors_diverging_spectral
pc.colors_diverging_BuRd
# ... and more
```

### Palette modifiers

```python
palette = pc.colors_journal_npg
palette.with_saturation(0.4)   # desaturate
palette.reversed()             # reverse order

# Create a custom palette
my_palette = pc.new_color_scheme("brand", ["#E63946", "#457B9D", "#1D3557"])
```

---

## Bundled Datasets

```python
pc.list_datasets()
# ['animals', 'climate', 'dinosaurs', 'distributions', 'energy',
#  'eu_countries', 'gene_expression', 'pca', 'spendings', 'study', 'time_course']

df = pc.load_dataset("gene_expression")
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
