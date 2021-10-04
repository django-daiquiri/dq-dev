#!/bin/bash

if [[ -f "/tmp/init.pid" ]]; then
    exit 1
fi

php-fpm7.4 --nodaemonize
