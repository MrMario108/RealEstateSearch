from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from realEstateSearch import settings as local
from .utils.worker import Worker
from .utils.scraper import Scraper
from .utils.database import Database
import requests

@shared_task(bind=True)
def send_mail_func(self, data = None):
    users = get_user_model().objects.all()
    for user in users:
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

@shared_task(bind=True)
def startScrap(self):
    """ Start scraping. Get parameters from db, prepare requests for all portals, and start worker"""
    print("\nClass: Starter; method: starter; \n")
    portalNames = ('olx',)
    allSearchParameters = Worker.getSearchParameters()
    for portalName in portalNames:
        requests = Worker.fromPortalName(portalName).execute(allSearchParameters)
        print("\nClass: Starter; method: starter; portalName, requests:", portalName, requests,"\n")
        worker.delay(portalName, requests)
    return "Started scrap"

@shared_task(bind=True)
def worker(self, portalName: str, requests):
    """You can use portalName to use different kinds of workers to get requests/urls
        This setting does not allow redirected ads to be scraped. It does not recognize the URL witch portal it is."""
    
    print('\nClass: ; method: worker; Start \n', file=open("log.txt", "a"))
    
    scrapType = 0 # scrap html with list of advertisement
    if requests != None:
        for request in requests:
            downloader.delay(portalName, scrapType,request)
    else:
        raise ValueError("Class: ; method: worker; messege: No requests")


@shared_task(bind=True)
def downloader(self, portalName, scrapType, requestsPuted):
    """Download html file and run scraper"""

    print('Class: ; method: downloader; msg = Start, portalName= ',portalName,"; url=",requestsPuted['url'], file=open("log.txt", "a"))

    ## for test - for prod leaf only else body
    htmlBody = None
    readExampleData(scrapType)
    if htmlBody:
        scraper(htmlBody, portalName, requestsPuted['params'])
    else:
        session = requests.Session()
        response = session.get(requestsPuted['url'], timeout=5)
        if response.status_code == 200:
            scraper.delay(portalName, scrapType, response.text, requestsPuted['params'])


@shared_task(bind=True)
def scraper(self, portalName, scrapType, response, params):
    """Run scraper if result is request run download, if result is scrap save data to database"""
    
    print('\nClass: ; method: scraper; Returned date: msg = Start scraper, worker_name= ',portalName, file=open("log.txt", "a"))
    scrapedDetail, portalName, requests = Scraper.fromPortalName(portalName, scrapType).execute(response, params)
      
    if scrapedDetail:
        print('Class: ; method: scraper; Returned date: msg = Try to save detail to database; scrap =',scrapedDetail, file=open("log.txt", "a"))
        Database.checkIfExists(scrapedDetail).execute()
    
    for request in requests:
        scrapType = 1
        downloader.delay(portalName, scrapType, request)

def readExampleData(scrapType):
    htmlBody = None
    if scrapType == 0:
        with open('olx-list.html', 'r') as f:
            htmlBody = f.read()
    elif scrapType == 1:
        with open('olx-detail.html', 'r') as f:
            htmlBody = f.read()
    return htmlBody