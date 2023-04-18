import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realEstateSearch.settings")

app = Celery("realEstateSearch")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule ={
    'scrap': {
        'task': 'scrapingApp.tasks.startScraperTasks',
        'schedule': 50*60.0,
    },
}

app.autodiscover_tasks()
