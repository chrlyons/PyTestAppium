.PHONY: setup test lint format clean run build deps update security

# Setup and Environment
setup:
	poetry install

# Dependency Management
deps:
	poetry lock --no-update
	poetry install

update:
	poetry update

# Code Quality and Formatting
lint:
	poetry run ruff check .
	poetry run black --check .
	poetry run isort --check-only .

format:
	poetry run isort .
	poetry run black .
	poetry run ruff check . --fix

# Testing and Coverage
test:
	poetry run pytest --cov-report html:cov_html --cov=src tests/ --html=report.html --self-contained-html

# Build
build:
	poetry build

# Cleanup
clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
	poetry cache clear pypi --all --no-interaction

# Security and Documentation
security:
	poetry check
