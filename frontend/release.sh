#!/usr/bin/env bash
#shellcheck disable=SC2039

set -euo pipefail

sudo apk update
sudo apk add --no-cache python3 make g++ yarn

yarn install --no-progress --frozen-lock
yarn eslint --config .eslintrc.prod.json src --ext .js,.jsx
yarn prettier --check src/
yarn test:ci
yarn build
