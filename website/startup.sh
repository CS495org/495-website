#!/bin/sh

python manage.py makemigrations
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_USER --email etbutton@crimson.ua.edu

# python manage.py check --deploy
# ^^ uncomment in prod

gunicorn --config gunicorn_config.py project.wsgi:application & \
celery -A project worker -l info -BE