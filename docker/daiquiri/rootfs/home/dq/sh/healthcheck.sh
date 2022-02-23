#!/bin/bash

pgrep caddy || exit 1

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    pgrep celery || exit 1
fi
