#!/bin/bash

reqfile="${DQAPP}/requirements.txt"
if [[ -f "${reqfile}" ]]; then
    echo "Install app requirements"
    pip install -r ${reqfile}
else
    echo "cannot pip install, file does not exist: ${reqfile}"
fi
