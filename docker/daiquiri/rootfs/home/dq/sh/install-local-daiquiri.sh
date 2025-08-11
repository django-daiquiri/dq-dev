#!/bin/bash
source "${HOME}/.bashrc"
source "${HOME}/.venv/bin/activate"

if [[ -d "$DQSOURCE" ]]; then
    echo "Installing local daiquiri"
    cd "${DQSOURCE}"
    uv pip install -e .[postgres,dev]

    nvm install
    npm ci
    npm run build
else
    echo "DQSOURCE is not defined"
fi
