#!/usr/bin/env bash
# Runs the shared contract-test suite against a running implementation.
#
# Usage:
#   CONTRACT_TEST_BASE_URL=http://localhost:8080/v1 \
#   CONTRACT_TEST_API_KEY=dev-local-key \
#   DATABASE_URL=postgres://polyglot:polyglot@localhost:5432/polyglot_api?sslmode=disable \
#   ./contract-tests/run.sh
#
# All three env vars have defaults matching local dev (see each
# implementation's README), so on a typical local setup you can just run it
# with no env vars set.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

./.venv/bin/pip install -q --upgrade pip
./.venv/bin/pip install -q -r requirements.txt

./.venv/bin/pytest "$@"
