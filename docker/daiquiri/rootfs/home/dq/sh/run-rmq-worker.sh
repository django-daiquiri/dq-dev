#!/bin/bash

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" != "true" ]]; then
    exit 255
fi

if [[ -f "${INIT_PID_FILE}" ]]; then
    exit 1
fi

queue="${1}"
concurrency="${2}"

if [[ -z "${queue}" ]]; then
    echo -e "\nA queue name is required. Please provide arg."
    echo -e "i.e. default, query or download"
    exit 1
fi

rundir="${HOME}/run"
mkdir -p "${rundir}"

cd "${DQAPP}"
echo "[$(date +%Y%m%d_%H%M%S)] Start rmq queue: ${queue}, concurrency ${concurrency}"
celery --app "config" worker \
    -Q "${queue}" \
    -c ${concurrency} \
    --pidfile="${rundir}/${queue}.pid" \
    --logfile="/dev/stdout" \
    --loglevel="${CELERYD_LOG_LEVEL}"
