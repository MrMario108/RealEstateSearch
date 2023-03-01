from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from realEstateSearch import settings as local

@shared_task()
def task_execute():

    print("Hello from Celery")


@shared_task(bind=True)
def send_mail_func(self, data = None):
    users = get_user_model().objects.all()
    for user in users:
        print(user.email)
        mail_subject = 'Hi! Celery testing'
        message = 'data scedule from RealEstateSearch'
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email= local.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False
        )
    return "Done"