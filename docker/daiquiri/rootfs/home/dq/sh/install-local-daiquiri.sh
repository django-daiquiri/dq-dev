#!/bin/bash

if [[ -d "$DQSOURCE" ]]; then
    cd "${DQSOURCE}"
    pip3 install -e "${DQSOURCE}"
else
    echo "DQSOURCE is not defined"
fi
