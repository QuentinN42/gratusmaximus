#!/usr/bin/env bash

set -euo pipefail

DOCKER_REPO="quentinn42/gratusmaximus"
DOCKER_HASH="$(git rev-parse HEAD)"
function push() {
    image="${DOCKER_REPO}:$(echo ${1} | rev | cut -d/ -f1 | rev)-${DOCKER_HASH}"
    echo "Building and pushing ${1} to ${image}"
    docker build --push --build-arg "SERVICE=${1}" -t "${image}" .
}

push maximus
(cd services && find gratters -maxdepth 1 -mindepth 1 -type d) |\
while read service; do
    push "${service}"
done

cd kube
set -o allexport
source .env
set +o allexport
terraform init -upgrade
terraform apply -var "hash=${DOCKER_HASH}"
