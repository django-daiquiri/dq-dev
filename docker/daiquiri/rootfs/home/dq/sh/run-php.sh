#!/bin/bash

if [[ -f "${INIT_PID_FILE}" ]]; then
    exit 1
fi

php-fpm7.4 --nodaemonize
