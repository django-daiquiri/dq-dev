#!/bin/bash
conf="${HOME}/conf/supervisord.conf"
spvcmd="supervisord -c \"${conf}\" ctl"

if [[ -z "${@}" ]]; then
    eval ${spvcmd} status
else
    eval ${spvcmd} ${@}
fi
