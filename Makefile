# Devlopement environement install
SHELL=/bin/bash -euo pipefail

SRC=sdk services

.PHONY: mypy ruff test clean migrate db db-wipe up seed deploy

uv.lock: pyproject.toml
	uv sync

# Code quality

ruff: uv.lock
	uv run python -m ruff check --fix $(SRC)

mypy: uv.lock
	uv run python -m mypy $(SRC)

test: uv.lock
	uv run python -m pytest -vvv $(SRC)

# Dev

up: migrate
	docker compose up --build -d --wait

down:
	docker compose down

clean:
	git clean -xdf

db:
	docker compose up -d --wait db

db-wipe:
	docker compose down -v

seed:
	docker compose up maximus --build -d
	docker compose exec maximus uv run python -m services.maximus.database.seed

migrate: db uv.lock
	uv run ./scripts/make_helpers.sh migrate

# Deploy

deploy:
	./scripts/deploy.sh
