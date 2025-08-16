.PHONY: help install test lint format clean build install-dev run-example
.DEFAULT_GOAL := help

# Variables
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
PACKAGE_NAME = markdown2pdf_resume_builder
SRC_DIR = src
TEST_DIR = tests
EXAMPLE_DIR = examples

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	$(PIP) install -e .

install-dev: ## Install development dependencies
	$(PIP) install -e ".[dev]"

install-docs: ## Install documentation dependencies
	$(PIP) install -e ".[docs]"

test: ## Run tests
	pytest $(TEST_DIR)/ -v

test-cov: ## Run tests with coverage
	pytest $(TEST_DIR)/ -v --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=html --cov-report=term

lint: ## Run linting checks
	flake8 $(SRC_DIR)/ $(TEST_DIR)/
	mypy $(SRC_DIR)/$(PACKAGE_NAME)/

format: ## Format code with black
	black $(SRC_DIR)/ $(TEST_DIR)/

format-check: ## Check code formatting
	black --check $(SRC_DIR)/ $(TEST_DIR)/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	$(PYTHON) -m build

run-example: ## Run example with sample resume
	$(PYTHON) -m $(PACKAGE_NAME) $(EXAMPLE_DIR)/resume_vibhor_janey_updated_aug_2025.md --one-page

run-example-full: ## Run example with sample resume (full version)
	$(PYTHON) -m $(PACKAGE_NAME) $(EXAMPLE_DIR)/resume_vibhor_janey_updated_aug_2025.md

docs-serve: ## Serve documentation locally
	mkdocs serve

docs-build: ## Build documentation
	mkdocs build

pre-commit: ## Run pre-commit checks
	pre-commit run --all-files

setup-dev: install-dev ## Set up development environment
	pre-commit install
	@echo "Development environment setup complete!"

check-all: format-check lint test ## Run all checks

# Release commands
version-patch: ## Bump patch version
	@echo "Current version: $$(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
	# Add version bumping logic here

version-minor: ## Bump minor version
	@echo "Current version: $$(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
	# Add version bumping logic here

version-major: ## Bump major version
	@echo "Current version: $$(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
	# Add version bumping logic here
