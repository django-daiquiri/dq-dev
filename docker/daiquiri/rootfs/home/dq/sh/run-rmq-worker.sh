#!/bin/bash

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" != "true" ]]; then
    exit 255
fi

if [[ -f "${INIT_PID_FILE}" ]]; then
    exit 1
fi

function sanitize_string() {
    echo "${1}" | tr '[:upper:]' '[:lower:]' | sed "s|[^a-z0-9_-]|_|g"
}

queue="${1}"
concurrency="${2}"

if [[ -z "${queue}" ]]; then
    echo -e "\nA queue name is required. Please provide arg."
    echo -e "i.e. default, query or download"
    exit 1
fi

rundir="${HOME}/run"
mkdir -p "${rundir}"
logdir="${HOME}/log"
mkdir -p "${logdir}"

cd "${DQAPP}"
echo "[$(date +%Y%m%d_%H%M%S)] Start rmq queue: ${queue}, concurrency ${concurrency}"
celery multi start ${queue} \
    -A config \
    -Q "${queue}" \
    -c ${concurrency} \
    --pidfile="${rundir}/$(sanitize_string ${queue}).pid" \
    --logfile="${logdir}/$(sanitize_string ${queue}).log" \
    --loglevel="${CELERYD_LOG_LEVEL}"
