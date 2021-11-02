#!/bin/bash

con="${HOME}/content"

mkdir -p "${con}"
if [[ ! -d "${con}/.git" ]]; then
    cd "${con}"
    git clone ${GIT_URL} .
else
    cd "${con}"
    git pull
fi
