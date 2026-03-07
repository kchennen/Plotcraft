.DEFAULT_GOAL := help
SHELL := /bin/bash

# ──────────────────────────────────────────────
#  Plotcraft — project management targets
# ──────────────────────────────────────────────

# ── Environment ──────────────────────────────

.PHONY: install
install: ## Install project + dev dependencies
	uv sync --all-groups

.PHONY: install-all
install-all: ## Install project + dev + all optional deps
	uv sync --all-groups --all-extras

.PHONY: update
update: ## Update all dependencies
	uv lock --upgrade
	uv sync --all-groups

# ── Quality ──────────────────────────────────

.PHONY: lint
lint: ## Run ruff linter
	uv run ruff check src/plotcraft tests

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	uv run ruff check --fix src/plotcraft tests

.PHONY: format
format: ## Format code with ruff
	uv run ruff format src/plotcraft tests

.PHONY: format-check
format-check: ## Check formatting without changes
	uv run ruff format --check src/plotcraft tests

.PHONY: typecheck
typecheck: ## Run mypy type checker
	uv run mypy src/plotcraft

.PHONY: check
check: lint format-check typecheck ## Run all checks (lint + format + types)

# ── Testing ──────────────────────────────────

.PHONY: test
test: ## Run test suite
	uv run pytest

.PHONY: test-fast
test-fast: ## Run tests excluding slow-marked ones
	uv run pytest -m "not slow"

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	uv run pytest --cov=plotcraft --cov-report=term-missing

.PHONY: test-cov-html
test-cov-html: ## Run tests with HTML coverage report
	uv run pytest --cov=plotcraft --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

.PHONY: test-visual
test-visual: ## Run visual regression tests
	uv run pytest --mpl -m mpl_image_compare

.PHONY: baseline
baseline: ## Regenerate visual test baselines
	uv run pytest --mpl-generate-path=tests/baseline \
		tests/test_geoms/

# ── Documentation ────────────────────────────

.PHONY: docs
docs: ## Build documentation
	uv run --extra docs mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve docs locally with live reload
	uv run --extra docs mkdocs serve

# ── Build & Publish ──────────────────────────

.PHONY: build
build: ## Build sdist + wheel
	uv build

.PHONY: clean
clean: ## Remove build artifacts and caches
	rm -rf dist/ build/ .ruff_cache/ .mypy_cache/ .pytest_cache/
	rm -rf htmlcov/ .coverage
	rm -rf src/plotcraft.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# ── CI shortcut ──────────────────────────────

.PHONY: ci
ci: check test ## Run full CI pipeline (checks + tests)

# ── Help ─────────────────────────────────────

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; \
		       {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
