#!/bin/sh

python manage.py runserver ${APP_HOST}:${APP_PORT}
python manage.py migrate


exec "$@"
