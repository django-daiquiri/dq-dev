#!/bin/bash

if [[ "${1}" == "--force" ]]; then
    export AUTO_PIP_INSTALL_APP_REQUIREMENTS="true"
fi

if [[ "$(echo ${AUTO_PIP_INSTALL_APP_REQUIREMENTS} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    reqfile="${DQAPP}/requirements.txt"
    if [[ -f "${reqfile}" ]]; then
        echo "Install app requirements"
        pip install -r ${reqfile} --force-reinstall
    else
        echo "cannot pip install, file does not exist: ${reqfile}"
    fi
else
    echo "auto pip install app requirements is disabled, use '--force' to do it anyway"
fi
