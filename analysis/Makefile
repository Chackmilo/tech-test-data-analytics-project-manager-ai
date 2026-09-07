# Run from analysis/. The repository root holds only the brief, the six
# deliverables, the given artifacts, and verify.py -- the one command those
# documents tell a reader to run.
.PHONY: help verify mutate test lint format all

PYTHON ?= python
ROOT := ..

help:
	@echo "Mythril Programme verification harness"
	@echo "  make verify   - run the 283-check deterministic audit"
	@echo "  make mutate   - run the 8-case mutation suite (proves the audit can fail)"
	@echo "  make test     - run pytest, or fall back to verify + mutate"
	@echo "  make lint     - ruff check"
	@echo "  make format   - ruff format"
	@echo "  make all      - verify then mutate"

verify:
	$(PYTHON) $(ROOT)/verify.py

mutate:
	$(PYTHON) mutation_test.py

test:
	@which pytest > /dev/null 2>&1 && pytest tests/ || ($(PYTHON) $(ROOT)/verify.py && $(PYTHON) mutation_test.py)

lint:
	@which ruff > /dev/null 2>&1 && ruff check mythril/ tests/ mutation_test.py $(ROOT)/verify.py || echo "ruff not found: pip install -e .[dev]"

format:
	@which ruff > /dev/null 2>&1 && ruff format mythril/ tests/ mutation_test.py $(ROOT)/verify.py || echo "ruff not found: pip install -e .[dev]"

all: verify mutate
