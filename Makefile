# Devlopement environement install
SHELL=/bin/bash -euo pipefail

PROJS=$(patsubst %/pyproject.toml,%/.pyproject.toml,$(shell find . -name pyproject.toml))
SRC=sdk services

SYSTEM_PYTHON=python3

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip --disable-pip-version-check
ACTIVATE=source $(VENV)/bin/activate

.PHONY: lint test clean migrate db db-wipe up seed deploy

up: migrate
	docker compose up --build -d --wait

down:
	docker compose down

lint: $(VENV) $(PROJS)
	$(PYTHON) -m ruff check --fix $(SRC)
	$(PYTHON) -m mypy $(SRC)

test: $(VENV) $(PROJS)
	$(PYTHON) -m pytest -vvv $(SRC)

clean:
	@echo $(PROJS)
	rm -rf .venv **/*.egg-info **/__pycache__ **/.pyproject.toml

db:
	docker compose up -d --wait db

db-wipe:
	docker compose down -v

seed:
	docker compose up maximus --build -d
	docker compose exec maximus ./scripts/seed.py

migrate: db $(VENV) $(PROJS)
	$(ACTIVATE) && ./scripts/make_helpers.sh migrate

.pyproject.toml: pyproject.toml
	$(PIP) install -e .[dev]
	cp "./pyproject.toml" "./.pyproject.toml"

%/.pyproject.toml: %/pyproject.toml
	$(PIP) install -e $(@D)[dev]
	cp "$(@D)/pyproject.toml" "$(@D)/.pyproject.toml"

$(VENV):
	$(SYSTEM_PYTHON) -m venv $(VENV)

deploy:
	./scripts/deploy.sh
