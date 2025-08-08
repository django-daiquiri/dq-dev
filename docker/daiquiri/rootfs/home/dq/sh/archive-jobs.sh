#!/bin/bash

cd ~/app
source "${UV_PROJECT_ENVIRONMENT}/bin/activate"
python manage.py archive_query_jobs -y -k 14d anonymous
deactivate
