#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $(pip3 freeze | grep -Poc "django-daiquiri") == "0" ]]; then
    cd "${DQSOURCE}" || exit 1
    pip3 install -e "${DQSOURCE}"

    cd "${DQAPP}"
    python3 manage.py makemigrations
    python3 manage.py migrate

    # silent because of the error message, that wp admin user already exists
    # necessary to create the daiquiri admin user
    python3 manage.py create_admin_user >/dev/null 2>&1

    mkdir -p "${DQAPP}/vendor"
    python3 manage.py download_vendor_files
    python3 manage.py collectstatic --no-input
    # python3 manage.py runserver 0.0.0.0:8000 &
else
    echo "Daiquiri is already installed."
fi
