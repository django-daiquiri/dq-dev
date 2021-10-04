#!/bin/bash

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" != "true" ]]; then
    echo "Async env var set to false. Won't run rabbitmq workers."
    exit 255
fi

if [[ -f "/tmp/init.pid" ]]; then
    exit 1
fi

worker="${1}"

if [[ -z "${worker}" ]]; then
    echo -e "\nA worker name is required. Please provide arg."
    echo -e "i.e. default, query or download"
    exit 1
fi

cd "${DQAPP}"
echo "Start rabbit mq worker: ${worker}"
python manage.py runworker ${worker}
