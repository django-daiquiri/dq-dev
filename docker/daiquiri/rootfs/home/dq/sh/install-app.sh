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

echo "makemigrations completed"

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

echo "npm done"

python manage.py collectstatic --no-input

if [[ "${SETUP_SCIENCE_DB}" == "True" ]]; then

    echo "- Create TAP schema"
    psql $DATABASE_DATA -c "CREATE SCHEMA IF NOT EXISTS ${TAP_SCHEMA};"
    psql $DATABASE_DATA -c "CREATE SCHEMA IF NOT EXISTS ${TAP_UPLOAD};"

    echo "- Create OAI schema"
    psql $DATABASE_DATA -c "CREATE SCHEMA IF NOT EXISTS ${OAI_SCHEMA};"

    cd ~/app/
    source "${UV_PROJECT_ENVIRONMENT}/bin/activate"
    echo "- Setup TAP schema"
    python manage.py migrate --database=tap

    echo "- Setup OAI schema"
    python manage.py migrate --database=oai

    echo "- Adding TAP schema in the metadata"
    python manage.py setup_tap_metadata

fi

