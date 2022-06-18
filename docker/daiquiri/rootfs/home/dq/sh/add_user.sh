#!/bin/bash

groupadd "${GNAME}"
if [[ ${UID} == 0 ]]; then
    useradd -m -s /bin/bash -g "${GNAME}" "${USER}"
else
    useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}"
fi

useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}"

chown -R "${USER}:${GID}" "${HOME}"
chmod -R 777 /tmp /var/log
