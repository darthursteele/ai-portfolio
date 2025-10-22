.PHONY: help install install-dev test test-cov lint format type-check pre-commit clean run-example docker-up docker-down docker-logs

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation targets
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

# Testing targets
test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=agentic --cov-report=html --cov-report=term-missing

test-fast: ## Run tests excluding slow tests
	pytest -m "not slow"

# Code quality targets
lint: ## Run linting checks
	flake8 agentic/ tests/
	mypy agentic/

format: ## Format code with black and isort
	black agentic/ tests/
	isort agentic/ tests/

format-check: ## Check code formatting without making changes
	black --check agentic/ tests/
	isort --check-only agentic/ tests/

type-check: ## Run type checking
	mypy agentic/

# Pre-commit targets
pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

# Development targets
clean: ## Clean up temporary files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run-research: ## Run the research crew example
	cd agentic && python examples/simple_research_crew.py

run-analysis: ## Run the content analysis crew example
	cd agentic && python examples/content_analysis_crew.py

run-writing: ## Run the creative writing crew example
	cd agentic && python examples/creative_writing_crew.py

# Docker targets
docker-build: ## Build Docker image
	docker-compose build

docker-up: ## Start development environment with Docker
	docker-compose up -d

docker-down: ## Stop Docker development environment
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-shell: ## Get shell in main container
	docker-compose exec ai-portfolio bash

docker-jupyter: ## Start Jupyter Lab
	docker-compose up -d jupyter
	@echo "Jupyter Lab available at http://localhost:8889"

docker-clean: ## Clean up Docker resources
	docker-compose down -v
	docker system prune -f

# Database targets
db-up: ## Start database services only
	docker-compose up -d chromadb redis postgres

db-down: ## Stop database services
	docker-compose stop chromadb redis postgres

# Environment setup
setup: install-dev pre-commit ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands"

# CI targets
ci: format-check lint type-check test ## Run all CI checks locally

# Release targets (future use)
version-patch: ## Bump patch version
	@echo "Version bumping not implemented yet"

version-minor: ## Bump minor version
	@echo "Version bumping not implemented yet"

version-major: ## Bump major version
	@echo "Version bumping not implemented yet"