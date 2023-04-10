#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
python manage.py migrate django_cron
pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py runcrons
