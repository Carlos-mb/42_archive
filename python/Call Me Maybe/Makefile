.PHONY: install run debug clean lint lint-strict

PYTHON := uv run python
MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install:
	uv sync

run:
	$(PYTHON) -m src

debug:
	CALLME_DEBUG=ON $(PYTHON) -m pdb -m src

clean:
	find . -path "./.venv" -prune -o -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf data/output

lint:
	uv run flake8 .
	uv run mypy . $(MYPY_FLAGS)

lint-strict:
	uv run flake8 .
	uv run mypy . --strict