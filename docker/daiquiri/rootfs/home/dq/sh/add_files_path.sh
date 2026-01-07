#!/bin/bash

sleep 5
source "${HOME}/.venv/bin/activate"

while true; do
    if [[ -f "${INIT_FINISHED_FILE}" ]]; then
        break
    fi
    sleep 1
done

conf="${HOME}/conf/fixture_files_path.json"

if python "${HOME}/app/manage.py" loaddata "${conf}" 2>/dev/null; then
    echo "✔ Fixtures for the 'cms' path loaded successfully."
else
    echo "✖ Failed to load fixtures for the 'cms' path. (Possible reason: The 'files' app is deactivated)."
fi
