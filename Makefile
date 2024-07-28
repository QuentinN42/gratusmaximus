# Devlopement environement install
SHELL=/bin/bash -euo pipefail -O globstar

PROJS=$(patsubst %/pyproject.toml,%/.pyproject.toml,$(shell find . -name pyproject.toml))
SRC=sdk services

SYSTEM_PYTHON=python3

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip --disable-pip-version-check

.PHONY: lint
lint: $(VENV) $(PROJS)
	$(PYTHON) -m ruff check --fix $(SRC)
	$(PYTHON) -m mypy $(SRC)

.PHONY: clean
clean:
	@echo $(PROJS)
	rm -rf .venv **/*.egg-info **/__pycache__ **/.pyproject.toml

.pyproject.toml: pyproject.toml
	$(PIP) install -e .[dev]
	cp "./pyproject.toml" "./.pyproject.toml"

%/.pyproject.toml: %/pyproject.toml
	$(PIP) install -e $(@D)[dev]
	cp "$(@D)/pyproject.toml" "$(@D)/.pyproject.toml"

$(VENV):
	$(SYSTEM_PYTHON) -m venv $(VENV)
