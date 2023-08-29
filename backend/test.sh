#!/usr/bin/env bash
# shellcheck disable=SC2155

set -eu

pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

python manage.py test
