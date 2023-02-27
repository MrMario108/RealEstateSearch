#!/bin/sh

until cd /RealEstateSearch
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A realEstateSearch.celery worker --loglevel=info --concurrency 1 -E