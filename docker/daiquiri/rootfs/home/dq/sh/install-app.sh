#!/bin/bash

source "${HOME}/.bashrc"
source "${HOME}/.venv/bin/activate"

reqfile="${DQAPP}/pyproject.toml"
echo "current directory: $(pwd)"

cd "${DQAPP}"

if [[ -f "${reqfile}" ]]; then
    
    # if the path to the local daiquiri repo exists then don't install it from the req
    if [[ -d "${DQSOURCE}" ]]; then
        echo "Install app requirements excluding daiquiri"
        uv pip install -e .
    else
        echo "Install app requirements"
        uv pip install -r ${reqfile} --extra daiquiri -e .
    fi
else
    echo "cannot pip install, file does not exist: ${reqfile}"
fi

python manage.py makemigrations
python manage.py migrate

if [[ "$(echo ${AUTO_CREATE_ADMIN_USER} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    # silent because of the error message that wp admin user already exists
    # necessary to create the daiquiri admin user
    python manage.py create_admin_user >/dev/null 2>&1
fi

if [[ -d "$DQSOURCE" ]] && [[ -f "${DQAPP}/package.json" ]]; then
    nvm use
    npm link ${DQSOURCE}
    npm run build
fi

python manage.py collectstatic --no-input
