#!/bin/bash
conf="${HOME}/conf/supervisord.conf"
spvcmd="supervisord -c \"${conf}\" ctl"

echo "spv.sh started at $(date)"

if [[ -z "${@}" ]]; then
    eval ${spvcmd} status
else
    eval ${spvcmd} ${@}
fi
