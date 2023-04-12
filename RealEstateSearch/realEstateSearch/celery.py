import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realEstateSearch.settings")

#  celery -A backend worker --loglevel=info -P gevent --concurrency 1 -E
app = Celery("realEstateSearch")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule ={
    'send-mail': {
        'task': 'scrapingApp.tasks.send_mail_func',
        'schedule': crontab(hour=9, minute=45), # 30.0
        'args' : ('dodatkowe dane z schedule',)
    },
    'scrap': {
        'task': 'scrapingApp.tasks.startScraperTasks',
        'schedule': 15.0,
    },
}

app.autodiscover_tasks()
