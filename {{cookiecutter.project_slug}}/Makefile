.PHONY: help install dev test test-all lint format typecheck clean run-api

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	uv sync

dev: ## Install all dependencies including dev tools
	uv sync --all-extras

test: ## Run unit tests only (fast, no IO)
	uv run pytest -v -m unit

test-all: ## Run all tests (unit + integration)
	uv run pytest -v

lint: ## Run linter (ruff check)
	uv run ruff check src/ tests/

format: ## Format code (ruff format + autofix)
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck: ## Run type checker (mypy)
	uv run mypy src/

clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf dist/ build/ *.egg-info/

run-api: ## Start the HTTP server (requires infrastructure/api/main.py to be implemented)
	uv run uvicorn {{ cookiecutter.project_slug }}.infrastructure.api.main:app --reload --port 8000

evaluate: ## Run agent evaluation script
	uv run python scripts/evaluate_agent.py
