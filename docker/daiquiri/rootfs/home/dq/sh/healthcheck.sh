#!/bin/bash

pgrep nginx || exit 1

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    pgrep -f celery || exit 1
fi
