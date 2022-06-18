#!/bin/bash

sleep 5

while true; do
    if [[ -f "${INIT_FINISHED_FILE}" ]]; then
        break
    fi
    sleep 1
done

conf="${HOME}/conf/fixture_files_path.json"

python "${HOME}/app/manage.py" loaddata "${conf}"
