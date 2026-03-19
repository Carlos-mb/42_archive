PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
MAIN ?= fly-in.py
SOURCES = common.py engine.py fly_in_map.py fly-in.py readconfig.py

.PHONY: install run debug lint lint-strict clean

define REQUIRE_MAP
	@if [ -z "$(MAP)" ]; then \
		echo "Error: MAP is required."; \
		echo "Usage: make $(1) MAP=<map_file>"; \
		exit 1; \
	fi
endef

install:
	$(PIP) install --upgrade pip mypy flake8

run:
	$(call REQUIRE_MAP,run)
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(call REQUIRE_MAP,debug)
	$(PYTHON) -m pdb $(MAIN) $(MAP)

lint:
	$(PYTHON) -m flake8 $(SOURCES)
	$(PYTHON) -m mypy $(SOURCES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 $(SOURCES)
	$(PYTHON) -m mypy $(SOURCES) --strict

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" \) -prune -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
