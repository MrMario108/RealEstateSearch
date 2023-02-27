import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realEstateSearch.settings")

#  celery -A backend worker --loglevel=info -P gevent --concurrency 1 -E
app = Celery("realEstateSearch")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
