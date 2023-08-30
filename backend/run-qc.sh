#!/usr/bin/env bash

set -eu

# ./wait-for-it.sh -h "${DB_HOST}" -p 5432 -- echo "Database is up and running"

set -eu

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

echo "Running tests"
COVERAGE_PROCESS_START=./.coveragerc \
  coverage run --parallel-mode --concurrency=multiprocessing --rcfile=./.coveragerc \
  manage.py test --shuffle --parallel 4 --verbosity=3

echo "Coverage"
coverage combine --rcfile=./.coveragerc
coverage report -m --rcfile=./.coveragerc

if [[ -n "${COVERALLS_REPO_TOKEN:-}" ]] ; then
  coveralls
fi

echo "Done"
