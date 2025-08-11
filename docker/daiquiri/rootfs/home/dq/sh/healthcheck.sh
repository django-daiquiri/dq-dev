#!/bin/bash
echo "healthcheck.sh started at $(date)"

pgrep nginx || exit 1

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    pgrep -f celery || exit 1
fi
