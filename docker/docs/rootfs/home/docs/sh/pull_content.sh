#!/bin/bash

con="${HOME}/content"

if [[ ! -f "${con}" ]]; then
    mkdir -p "${con}"
    cd "${con}"
    git clone ${GIT_URL} .
else
    cd "${con}"
    git pull
fi
