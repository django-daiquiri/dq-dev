#!/bin/bash
source "${HOME}/.venv/bin/activate"

while [ ! -f  "${INIT_FINISHED_FILE}" ]; do
  echo "Waiting for init to complete..."
  sleep 2
done

if [[ -f "${HOME}/conf/nginx.conf" ]]; then
    nginx -c "${HOME}/conf/nginx.conf" -g "daemon off;"
else
    echo "Missing NGINX config: ${HOME}/conf/nginx.conf"
    exit 1
fi
