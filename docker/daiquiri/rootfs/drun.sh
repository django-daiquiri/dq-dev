#!/bin/bash

${HOME}/sh/render_supervisord_conf.sh
${HOME}/bin/supervisord -c "${HOME}/conf/supervisord.conf"
