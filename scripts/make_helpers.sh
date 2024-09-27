#!/usr/bin/env bash

set -euo pipefail

function new_migration() {
    echo -n "Enter Migration name: "
    read name
    alembic revision --autogenerate -m "${name}"
}

function migrate() {
    cd services/maximus
    alembic upgrade head
    alembic check || new_migration
}

if [ -z "$1" ];
then
    echo "Missing action"
    exit 1
else
    $@
fi
