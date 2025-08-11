#!/bin/bash
echo "add_files_path.sh started at $(date)"

sleep 5
source "${HOME}/.venv/bin/activate"

while true; do
    if [[ -f "${INIT_FINISHED_FILE}" ]]; then
        break
    fi
    sleep 1
done

conf="${HOME}/conf/fixture_files_path.json"

uv run python3 "${HOME}/app/manage.py" loaddata "${conf}"
