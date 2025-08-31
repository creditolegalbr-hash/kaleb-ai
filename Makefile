# Makefile for Intelligent Automation System

# Variables
PYTHON := python3
PIP := pip
PROJECT_NAME := intelligent-automation-system
TEST_DIR := tests
SRC_DIR := src

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run the application"
	@echo "  test        - Run all tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  clean       - Clean build artifacts"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run application in Docker"
	@echo "  docker-test  - Run tests in Docker"
	@echo "  docs         - Generate documentation"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with autopep8"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov autopep8

# Run the application
.PHONY: run
run:
	$(PYTHON) $(SRC_DIR)/main.py

# Run tests
.PHONY: test
test:
	$(PYTHON) $(TEST_DIR)/run_tests.py

# Run tests with coverage
.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term

# Clean build artifacts
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info/
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/

# Docker commands
.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run:
	docker run --rm -it $(PROJECT_NAME)

.PHONY: docker-test
docker-test:
	docker run --rm -it -v $(PWD):/app $(PROJECT_NAME) python tests/run_tests.py

# Documentation
.PHONY: docs
docs:
	@echo "Documentation is available in docs/implemented_features.md"

# Linting
.PHONY: lint
lint:
	@echo "Installing pylint if not present..."
	@$(PIP) install pylint >/dev/null 2>&1 || true
	pylint $(SRC_DIR)/*.py $(SRC_DIR)/agents/*.py $(SRC_DIR)/pipelines/*.py $(SRC_DIR)/integrations/*.py $(SRC_DIR)/config/*.py

# Code formatting
.PHONY: format
format:
	@echo "Installing autopep8 if not present..."
	@$(PIP) install autopep8 >/dev/null 2>&1 || true
	autopep8 --in-place --recursive --select=E1,E2,E3,E4,E5,W1,W2,W3,W6 $(SRC_DIR) $(TEST_DIR)

# Package the application
.PHONY: package
package:
	$(PYTHON) setup.py sdist bdist_wheel

# Install the package locally
.PHONY: install-package
install-package:
	$(PIP) install -e .

# Show project information
.PHONY: info
info:
	@echo "Project: $(PROJECT_NAME)"
	@echo "Source directory: $(SRC_DIR)"
	@echo "Test directory: $(TEST_DIR)"
	@echo "Python version: $$(python --version 2>&1)"