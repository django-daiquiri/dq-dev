#!/bin/bash

folder_env_var_list=(
    "ARCHIVE_BASE_PATH"
    "ARCHIVE_DOWNLOAD_DIR"
    "FILES_BASE_PATH"
    "LOG_DIR"
    "QUERY_DOWNLOAD_DIR"
    "QUERY_UPLOAD_DIR"
)

function env_var_set() {
    var=$(echo "${1}" | tr '[:lower:]' '[:upper:]')
    if [[ -n $(eval "echo \${$var}") ]]; then
        echo "true"
    else
        echo "false"
    fi
}

function folder_exists() {
    if [[ -d "${1}" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

for var in "${folder_env_var_list[@]}"; do
    fol=$(eval "echo \${$var}")
    if [[ $(env_var_set "${var}") == "true" && \
    $(folder_exists "${fol}") == "false" ]]; then
        echo "Create folder ${fol}"
        mkdir -p "${fol}"
    fi
done
