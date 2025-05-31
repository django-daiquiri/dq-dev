#!/bin/bash


source "${HOME}/.bashrc"
source "${HOME}/.venv/bin/activate"

reqfile="${DQAPP}/pyproject.toml"
echo "current directory: $(pwd)"


if [[ -f "${reqfile}" ]]; then
    cd "${DQAPP}"

    # if the path to the local daiquiri repo exists then don't install it from the req
    if [[ -d "${DQSOURCE}" ]]; then
        echo "Install app requirements excluding daiquiri"
        uv pip install -e .
        uv pip list
    else
        echo "Install app requirements"
        # uv pip install -r ${reqfile}
        uv pip install -e .
    fi
else
    echo "cannot pip install, file does not exist: ${reqfile}"
fi

uv run manage.py makemigrations
uv run manage.py migrate

if [[ "$(echo ${AUTO_CREATE_ADMIN_USER} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    # silent because of the error message, that wp admin user already exists
    # necessary to create the daiquiri admin user
    uv run manage.py create_admin_user >/dev/null 2>&1
fi

nvm use
npm link ${DQSOURCE}
npm run build

# mkdir -p "${DQAPP}/vendor"
# python3 manage.py download_vendor_files
#
uv run manage.py collectstatic --no-input
