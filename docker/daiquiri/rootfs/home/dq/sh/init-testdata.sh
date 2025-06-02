#!/bin/bash
set -e
cd "${DQAPP}"
source "${HOME}/.venv/bin/activate"

python manage.py sqlcreate
python manage.py sqlcreate --test
python manage.py sqlcreate --schema=daiquiri_data_obs

python manage.py download_vendor_files
python manage.py test daiquiri --keepdb
python manage.py migrate
python manage.py migrate --database=data
python manage.py loaddata ../source/testing/fixtures/*
