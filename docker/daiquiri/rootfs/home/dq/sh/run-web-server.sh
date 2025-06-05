#!/bin/bash

if [[ ! -f "${INIT_FINISHED_FILE}" ]]; then
    exit 1
fi

cd "${DQAPP}"
if [[ -z "$(ps aux | grep "[g]unicorn")" ]]; then
    if [[ "$(echo "${ENABLE_GUNICORN}" | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
        gunicorn --bind 0.0.0.0:8000 \
            --log-file=/dev/stdout \
            --access-logfile=/dev/stdout \
            --worker-class gthread \
            --workers 2 \
            --threads 8 \
            config.wsgi:application
    else
        # django dev server for development, has auto reload, does not cache
        python3 manage.py runserver 0.0.0.0:8000
    fi
fi
