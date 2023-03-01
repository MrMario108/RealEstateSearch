#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python3 manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email m.majewski108@gmail.com \
        --preserve

uwsgi --socket :9000 --workers 4 --master --enable-threads --module realEstateSearch.wsgi