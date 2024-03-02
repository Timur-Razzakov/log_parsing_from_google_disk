#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate --no-input

# run project
python manage.py runserver 0.0.0.0:8000
