#!/bin/bash

if [[ -d "$DQSOURCE" ]]; then
    cd "${DQSOURCE}"
    pip3 install -e "${DQSOURCE}"

    nvm install
    npm ci
    npm run build
else
    echo "DQSOURCE is not defined"
fi
