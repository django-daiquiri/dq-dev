#!/bin/bash


source "${HOME}/.bashrc"

reqfile="${DQAPP}/requirements.txt"

if [[ -f "${reqfile}" ]]; then
    # if the path to the local daiquiri repo exists then don't install it from the req
    if [[ -d "${DQSOURCE}" ]]; then
        echo "Install app requirements excluding daiquiri"
        pip install $(grep -v "^\s*#" ${reqfile} | grep -ivE "django-daiquiri")
    else
        echo "Install app requirements"
        pip install -r ${reqfile}
    fi
else
    echo "cannot pip install, file does not exist: ${reqfile}"
fi

cd "${DQAPP}"
python3 manage.py makemigrations
python3 manage.py migrate

if [[ "$(echo ${AUTO_CREATE_ADMIN_USER} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    # silent because of the error message, that wp admin user already exists
    # necessary to create the daiquiri admin user
    python3 manage.py create_admin_user >/dev/null 2>&1
fi

if [[ -d "$DQSOURCE" ]] && [[ -f "${DQAPP}/package.json" ]]; then
    nvm use
    npm link ${DQSOURCE}
    npm run build
fi

python3 manage.py collectstatic --no-input
