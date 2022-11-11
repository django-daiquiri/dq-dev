#!/bin/bash

function make_docs_symlink() {
    docs_dir="${HOME}/docs"
    fol="$(echo "${1}" | grep -Po ".*(?=\/)")"
    mkdir -p "${fol}"
    if [[ (! -L "${1}" && -d "${docs_dir}/.git") ]]; then
        ln -s "${docs_dir}/cms" "${1}"
    fi

}

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

make_docs_symlink "${FILES_BASE_PATH}/cms"
make_docs_symlink "${CADDY_SENDFILE_ROOT}/files/cms"
