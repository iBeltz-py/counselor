#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python world_champ_2022/manage.py createsuperuser --no-input

