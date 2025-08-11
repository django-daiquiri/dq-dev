#!/bin/bash
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

# execute custom scripts (up)
echo "Looking for custom scripts to execute..."
CUSTOM_SCRIPTS=$(find /tmp -type f -executable -regex ".*\/custom_scripts\/up.*" | sort)
if [ -n "$CUSTOM_SCRIPTS" ]; then
  echo "Found custom scripts to execute:"
  echo "$CUSTOM_SCRIPTS" | sed 's/^/  /'
  echo "Executing custom scripts..."
  echo "$CUSTOM_SCRIPTS" | xargs -i /bin/bash {}
else
  echo "No custom scripts found to execute."
fi

echo "finished at $(date)" >"${INIT_FINISHED_FILE}"
