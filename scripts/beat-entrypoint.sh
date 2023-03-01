#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
        sleep 2
done
# run celery beat
celery -A realEstateSearch.celery beat -l info