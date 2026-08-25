#!/bin/bash

if [[ "${BUILD_RELEASE}" != "1" ]]; then
    exit 0
fi

set -e

stop_supervisord() {
    exit_code=$?
    echo "Stopping supervisord..."
    "${HOME}/sh/spv.sh" shutdown || true
    exit "${exit_code}"
}

trap stop_supervisord EXIT

source "${HOME}/.bashrc"
source "${HOME}/.venv/bin/activate"

echo "Waiting for Daiquiri initialization..."
while [ ! -f "${INIT_FINISHED_FILE}" ]; do sleep 1; done

cd "${DQSOURCE}"
echo "Cleaning dist/"
rm -rf dist/*

echo "Installing release dependencies..."
/home/dq/.local/bin/uv pip install -e ".[postgres,dev]"

echo "Building Daiquiri release..."
daiquiri-admin build

echo "Checking release files..."
twine check dist/*

echo "Daiquiri release built successfully"
