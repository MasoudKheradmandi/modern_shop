#!/bin/sh

set -e

cd /app/

POETRY_RUN='poetry run'

echo 'Collecting static files...'
$POETRY_RUN python3 manage.py collectstatic --no-input

echo 'Running migrations...'
$POETRY_RUN python3 manage.py migrate --no-input

echo 'Running server...'
$POETRY_RUN gunicorn core.wsgi --bind 0.0.0.0:8000