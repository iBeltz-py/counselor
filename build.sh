#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py crontab add
python manage.py crontab show
python manage.py collectstatic --no-input
python manage.py migrate
