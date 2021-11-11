#!/bin/bash

docs_dir="${HOME}/docs"
sl_target="${FILES_BASE_PATH}/cms"

if [[ -n "${DOCS_GIT_URL}" ]]; then
    mkdir -p "${docs_dir}"
    if [[ ! -d "${docs_dir}/.git" ]]; then
        cd "${docs_dir}"
        git clone ${DOCS_GIT_URL} .
    else
        cd "${docs_dir}"
        git pull
    fi
fi

if [[ (! -L "${sl_target}" && -d "${docs_dir}/.git") ]]; then
    ln -s "${docs_dir}/cms" "${sl_target}"
fi
