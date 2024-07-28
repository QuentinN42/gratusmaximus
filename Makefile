# Devlopement environement install
SHELL=/bin/bash -euo pipefail -O globstar

PROJS=$(shell find . -name pyproject.toml -exec dirname {} \;)
SRC=sdk services

SYSTEM_PYTHON=python3

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip --disable-pip-version-check

.PHONY: lint
lint: $(VENV) $(PROJS)
	$(PYTHON) -m ruff check --fix $(SRC)
	$(PYTHON) -m mypy $(SRC)

%: $(VENV)
	$(PIP) install -e $@[dev]

Makefile: ;

$(VENV):
	$(SYSTEM_PYTHON) -m venv $(VENV)
