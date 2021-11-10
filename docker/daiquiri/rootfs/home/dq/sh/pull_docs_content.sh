#!/bin/bash

if [[ -n "${DOCS_GIT_URL}" ]]; then
    docs_dir="${HOME}/docs"
    mkdir -p "${docs_dir}"
    if [[ ! -d "${docs_dir}/.git" ]]; then
        cd "${docs_dir}"
        git clone ${DOCS_GIT_URL} .
    else
        cd "${docs_dir}"
        git pull
    fi
fi
