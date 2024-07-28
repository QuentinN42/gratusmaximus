# Devlopement environement install
SHELL=/bin/bash -euo pipefail -O globstar

PROJS=$(shell find . -name pyproject.toml -exec dirname {} \; | grep -v egg-info)

SYSTEM_PYTHON=python3

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: lint
lint: $(VENV) $(PROJS)
	@echo $^
	$(PYTHON) -m ruff check --fix sdk services
	$(PYTHON) -m mypy sdk services

%: $(VENV) %/pyproject.toml
	$(PIP) install -e $@[dev]

$(VENV):
	$(SYSTEM_PYTHON) -m venv $(VENV)
