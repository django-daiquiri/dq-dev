#!/bin/bash

${HOME}/sh/install-app-requirements.sh
${HOME}/sh/install-daiquiri.sh

if [[ "$(echo ${PIP_FORCE_REINSTALL_APP_REQUIREMENTS} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    ${HOME}/sh/install-app-requirements.sh --force
fi

python3 ${HOME}/py/render_supervisord_conf.py
${HOME}/bin/supervisord -c "${HOME}/conf/supervisord.conf"
