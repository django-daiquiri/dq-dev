#!/bin/bash

source "${HOME}/.bashrc"

echo $$ >"/tmp/init.pid"

${HOME}/sh/install-caddy.sh
${HOME}/sh/install-daiquiri.sh

cd "${DQAPP}" || exit 1

sfil="${HOME}/tpl/wsgi.py"
tfil="${DQAPP}/config/wsgi.py"
if [[ ! -f "${tfil}" ]]; then
    copy -f "${sfil}" "${tfil}"
fi

# render config files
if [[ ! -f "${WORDPRESS_PATH}/wp-config.php" ]]; then
    ${HOME}/sh/expand-env-vars.sh \
        "${HOME}/tpl/wp-config.php" "${WORDPRESS_PATH}/wp-config.php"
fi

${HOME}/sh/expand-env-vars.sh \
    "${HOME}/tpl/Caddyfile.tpl" "${HOME}/Caddyfile"

${HOME}/sh/init-wordpress.sh

if [[ "${ASYNC}" == "True" ]]; then
    ${HOME}/sh/init-folders.sh
fi

# execute custom scripts
find /tmp -type f -executable -regex ".*\/custom_scripts\/up.*" |
    sort | xargs -i /bin/bash {}

rm -f "/tmp/init.pid"
