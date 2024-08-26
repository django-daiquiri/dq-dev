#!/bin/bash

if [[ -d $DQSOURCE ]]; then
    ${HOME}/sh/install-local-daiquiri.sh
fi

${HOME}/sh/install-app.sh

python3 ${HOME}/py/render_supervisord_conf.py
${HOME}/bin/supervisord -c "${HOME}/conf/supervisord.conf"
