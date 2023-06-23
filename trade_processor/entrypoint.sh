#!/bin/sh

python manage.py migrate
gunicorn config.wsgi:application --bind ${APP_HOST}:${APP_PORT:}

exec "$@"
