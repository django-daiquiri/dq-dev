#!/bin/bash

if [[ -f "${HOME}/conf/nginx.conf" ]]; then
    nginx -c "${HOME}/conf/nginx.conf" -g "daemon off;"
else
    echo "Missing NGINX config: ${HOME}/conf/nginx.conf"
    exit 1
fi
