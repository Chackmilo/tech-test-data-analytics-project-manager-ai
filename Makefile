.PHONY: help verify mutate test lint format all

PYTHON ?= python

help:
	@echo "Mythril Programme Verification & Engineering Harness"
	@echo "====================================================="
	@echo "Available commands:"
	@echo "  make verify   - Run the 276-check deterministic verification audit"
	@echo "  make mutate   - Run the 8-case adversarial mutation test suite"
	@echo "  make test     - Run tests via pytest (or fallback to verify + mutate)"
	@echo "  make lint     - Check code quality with ruff (if installed)"
	@echo "  make format   - Auto-format code with ruff (if installed)"
	@echo "  make all      - Run verification and mutation tests"

verify:
	$(PYTHON) verify.py

mutate:
	$(PYTHON) mutation_test.py

test:
	@which pytest > /dev/null 2>&1 && pytest tests/ || $(PYTHON) verify.py && $(PYTHON) mutation_test.py

lint:
	@which ruff > /dev/null 2>&1 && ruff check src/ tests/ verify.py mutation_test.py || echo "Ruff not found. Install dev dependencies with pip install -e .[dev]"

format:
	@which ruff > /dev/null 2>&1 && ruff format src/ tests/ verify.py mutation_test.py || echo "Ruff not found. Install dev dependencies with pip install -e .[dev]"

all: verify mutate
