#!/bin/bash
source ${HOME}/.bashrc

if [[ -d $DQSOURCE ]]; then
    bash ${HOME}/sh/install-local-daiquiri.sh
fi

${HOME}/sh/install-app.sh

echo "app installed"

uv run python3 ${HOME}/py/render_supervisord_conf.py
echo "supervisord conf rendered"
${HOME}/bin/supervisord -c "${HOME}/conf/supervisord.conf"
echo "supervisord started"