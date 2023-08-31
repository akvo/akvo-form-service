#!/usr/bin/env bash
#shellcheck disable=SC2039

set -exuo pipefail

IMAGE_PREFIX="eu.gcr.io/akvo-lumen/akvo-form-service"
CI_COMMIT=$(git rev-parse --short "$GITHUB_SHA")

echo "CI_COMMIT=${CI_COMMIT}"

dc() {
    docker compose \
        --ansi never \
        "$@"
}

frontend_build() {

    echo "PUBLIC_URL=/" >frontend/.env

    # Code Quality and Build Folder
    sed 's/"warn"/"error"/g' <frontend/.eslintrc.json >frontend/.eslintrc.prod.json

    dc -f docker-compose.yml run \
        --rm \
        --no-deps \
        frontend \
        sh release.sh

    docker build \
        --tag "${IMAGE_PREFIX}/frontend:latest" \
        --tag "${IMAGE_PREFIX}/frontend:${CI_COMMIT}" frontend

}

backend_build() {

    docker build \
        --tag "${IMAGE_PREFIX}/backend:latest" \
        --tag "${IMAGE_PREFIX}/backend:${CI_COMMIT}" backend

    # Code Quality
    dc -f docker-compose.ci.yml -p backend-test run \
        --rm \
        backend ./run-qc.sh
}

backend_build
frontend_build
