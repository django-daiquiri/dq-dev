#!/bin/bash

source "${HOME}/.bashrc"

if [[ -f "${INIT_FINISHED_FILE}" ]]; then
  exit
fi

mkdir -p "${FILES_BASE_PATH}"

cd "${DQAPP}" || exit 1

sfil="${HOME}/tpl/wsgi.py"
tfil="${DQAPP}/config/wsgi.py"
if [[ ! -f "${tfil}" ]]; then
  copy -f "${sfil}" "${tfil}"
fi

mkdir -p /tmp/nginx/client_body \
         /tmp/nginx/proxy \
         /tmp/nginx/fastcgi \
         /tmp/nginx/uwsgi \
         /tmp/nginx/scgi
envsubst '${SENDFILE_URL} ${FILES_BASE_PATH} ${EXPOSED_PORT} ${DQAPP}' <"${HOME}/tpl/nginx.conf" >"${HOME}/conf/nginx.conf"

if [[ "${ASYNC}" == "True" ]]; then
  ${HOME}/sh/init-folders.sh
fi

# execute custom scripts (up)
find /tmp -type f -executable -regex ".*\/custom_scripts\/up.*" |
  sort | xargs -i /bin/bash {}

echo "finished at $(date)" >"${INIT_FINISHED_FILE}"
