#!/bin/bash

source "${HOME}/.bashrc"

if [[ -d "$DQSOURCE" ]]; then
    cd "${DQSOURCE}"
    pip3 install -e .[postgres,dev]

    nvm install
    npm ci
    npm run build
else
    echo "DQSOURCE is not defined"
fi
