#!/bin/bash

export GIT_TERMINAL_PROMPT=0
content_dir="${HOME}/docs"

function make_content_symlink() {
  fol="$(echo "${1}" | grep -Po ".*(?=\/)")"
  mkdir -p "${fol}"
  if [[ (! -L "${1}" && -d "${content_dir}/.git") ]]; then
    ln -s "${content_dir}/cms" "${1}"
  fi

}

if [[ -n "${DOCS_GIT_URL}" ]]; then
  mkdir -p "${content_dir}"
  if [[ ! -d "${content_dir}/.git" ]]; then
    cd "${content_dir}"
    git clone ${DOCS_GIT_URL} .
  else
    cd "${content_dir}"
    git pull
  fi
fi

make_content_symlink "${FILES_BASE_PATH}/cms"
