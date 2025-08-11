#!/bin/bash
echo "init_all.sh started at $(date)"

source "${HOME}/.bashrc"
source "${HOME}/.venv/bin/activate"

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

${HOME}/sh/init-folders.sh

echo "executing custom scripts (up)"
echo "lol" 
# # execute custom scripts (up)
# find /tmp -type f -executable -regex ".*\/custom_scripts\/up.*" |
#   sort | xargs -i /bin/bash {}

echo "finished at $(date)" >"${INIT_FINISHED_FILE}"
