#!/bin/bash

${HOME}/sh/install-daiquiri.sh
${HOME}/sh/install-app-requirements.sh

python3 ${HOME}/py/render_supervisord_conf.py
${HOME}/bin/supervisord -c "${HOME}/conf/supervisord.conf"
