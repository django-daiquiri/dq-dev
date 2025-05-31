#!/bin/bash
set -e
cd "${DQAPP}"
source "${HOME}/.venv/bin/activate"

uv run ./manage.py sqlcreate
uv run ./manage.py sqlcreate --test
uv run ./manage.py sqlcreate --schema=daiquiri_data_obs

uv run ./manage.py download_vendor_files
uv run ./manage.py test daiquiri --keepdb
uv run ./manage.py migrate
uv run ./manage.py migrate --database=data
uv run ./manage.py loaddata ../source/testing/fixtures/*
