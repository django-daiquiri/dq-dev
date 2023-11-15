#!/bin/bash

source "${HOME}/.bashrc"

if [[ -f "${INIT_FINISHED_FILE}" ]]; then
  exit
fi

mkdir -p "${FILES_BASE_PATH}"

# ${HOME}/sh/install-daiquiri.sh
# ${HOME}/sh/install-app-requirements.sh

cd "${DQAPP}" || exit 1

sfil="${HOME}/tpl/wsgi.py"
tfil="${DQAPP}/config/wsgi.py"
if [[ ! -f "${tfil}" ]]; then
  copy -f "${sfil}" "${tfil}"
fi

# render config files
cat "${HOME}/tpl/Caddyfile" | envsubst >"${CADDYFILE}"

if [[ "${ASYNC}" == "True" ]]; then
  ${HOME}/sh/init-folders.sh
fi

# execute custom scripts (up)
find /tmp -type f -executable -regex ".*\/custom_scripts\/up.*" |
  sort | xargs -i /bin/bash {}

echo "finished at $(date)" >"${INIT_FINISHED_FILE}"
