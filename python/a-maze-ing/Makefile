.PHONY: install run debug clean lint lint-strict

PYTHON ?= python3
PIP ?= pip
MAIN ?= a_maze_ing.py
CONFIG ?= config.txt

install:
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "No requirements.txt found. Skipping dependency installation."; \
	fi
	$(PIP) install --upgrade --force-reinstall .

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	@echo "Instalando la herramienta de construcción..."
	$(PIP) install --upgrade build
	@echo "Generando los archivos .whl y .tar.gz..."
	$(PYTHON) -m build
	@echo "Moviendo los paquetes a la raíz del repositorio..."
	mv dist/*.whl .
	mv dist/*.tar.gz .
	@echo "Limpiando carpetas temporales de compilación..."
	rm -rf dist/ build/ *.egg-info/
	@echo "¡Listo! Tu paquete está en la raíz preparado para la entrega."
