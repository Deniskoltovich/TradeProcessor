#!/bin/sh

python manage.py migrate
python manage.py runserver ${APP_HOST}:${APP_PORT}

exec "$@"
