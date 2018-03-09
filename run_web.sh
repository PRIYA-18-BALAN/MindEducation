#!/bin/sh

python manage.py collectstatic --noinput&&python manage.py migrate&&/usr/local/bin/gunicorn MentalHealth.wsgi:application --reload -w 2 -b :80