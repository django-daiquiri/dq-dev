#!/bin/bash

source "${HOME}/.bashrc"
cd "${HOME}"

if [[ -d "$DQSOURCE" ]]; then
    echo "Installing local daiquiri"
    cd "${DQSOURCE}"
    # source "${HOME}/.venv/bin/activate"
    uv pip install -e .[postgres]
    # uv pip list

    nvm install
    npm ci
    npm run build
else
    echo "DQSOURCE is not defined"
fi
