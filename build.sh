#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py migrate django_cron
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py runcrons
