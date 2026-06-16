PYTHON := python3
CONFIG ?= default.json
ENTRYPOINT := pac-man.py
WHL ?=
UV_RUN := uv run
ifneq ($(strip $(WHL)),)
UV_RUN += --with "$(WHL)"
endif

.PHONY: install run debug clean lint help

.DEFAULT_GOAL := help

install:
	uv sync --dev

run:
	$(UV_RUN) $(PYTHON) $(ENTRYPOINT) $(CONFIG)

debug:
	$(UV_RUN) $(PYTHON) -m pdb $(ENTRYPOINT) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf build dist *.egg-info

lint:
	uv run flake8 pac-man.py src/.
	uv run mypy pac-man.py  src/. --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

help:
	@echo "Usage:"
	@echo "  make run                  # run with default dependencies"
	@echo "  make run WHL=path/to.whl  # run with an extra wheel installed by uv"