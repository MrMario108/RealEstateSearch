from celery import shared_task

@shared_task()
def task_execute():

    print("Hello from Celery")
