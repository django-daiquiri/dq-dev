#!/bin/bash

force_reinstall=""

if [[ "${1}" == "--force" ]]; then
    force_reinstall="--force-reinstall"
fi

reqfile="${DQAPP}/requirements.txt"
if [[ -f "${reqfile}" ]]; then
    echo "Install app requirements"
    pip install -r ${reqfile} ${force_reinstall}
else
    echo "cannot pip install, file does not exist: ${reqfile}"
fi
