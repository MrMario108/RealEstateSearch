import logging
import requests
from celery import shared_task
from .utils.abstractScraper import AbstractScraper
from .utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

logger = logging.getLogger('celeryLogger')


@shared_task(bind=True)
def sendMail(self, realEstateDetails = None):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = 'Real Estate Search'
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=prepareMailMessage(realEstateDetails),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False
        )

def prepareMailMessage(realEstateDetails):
    if realEstateDetails != None:
        message = 'We found a new real estate ! \n'
        message += realEstateDetails["title"]+'\n'
        message += 'City: ' + realEstateDetails["city"]+'\n'
        message += 'Price: ' + realEstateDetails["price"]+'\n'
        message += realEstateDetails["category"]
        message += 'Rooms: ' + realEstateDetails["rooms"]+'\n'
        message += 'Click link: ' + realEstateDetails["link"]
        return message
    else:
        return 'We found a new real estate !!! Please login to your account to check details.'

class GroupedSearchParameters():
    
    def get(self) -> list:
        """ Groups parameters to limit the number of web pages scraped and the number of properties found """
        groupedSearchParameters = []
        category = Category.objects.all()
        cities = City.objects.all()
        
        for cat in category:
            for city in cities:
                finded = self.findMaxPrice(cat, city)
                if finded != None:
                    groupedSearchParameters.append(finded)

        logger.info("getGroupedSearchParameters; returned values: "+ str(groupedSearchParameters))

        return groupedSearchParameters

    def joinSingleSearchParametersFrom(self, selectedParameters, maxPrice):

        selectedParameters[0]["price"] = maxPrice['price__max']
        logger.info("joinSingleSearchParametersFrom: " + str(selectedParameters[0]))
        return selectedParameters[0]

    def findPricesForCategoryAndCity(self, category, city):
        return SearchingSettings.objects.filter(category__categoryName = category.categoryName, city__slug = city.slug).values('area', 'rooms', 'price', 'city__slug', 'category__categoryName')

    def findMaxPrice(self, category, city):
        selectedParameters = self.findPricesForCategoryAndCity(category, city)
        logger.info("getGroupedSearchParameters; selectedParameters: " + str(selectedParameters))
        maxPrice = selectedParameters.aggregate(Max('price'))
        logger.info("getGroupedSearchParameters; maxPrice: " + str(maxPrice))
        if (maxPrice['price__max'] != None):
            return self.joinSingleSearchParametersFrom(list(selectedParameters), maxPrice)

@shared_task(bind=True)
def saveRealEstateDetails(self, realEstateDetails):
    if SaveApartment.checkIfExists(realEstateDetails).tryToSave():
        sendMail(realEstateDetails)



@shared_task(bind=True)
def downloadHtml(self, url) -> str:
    session = requests.Session()
    response = session.get(url, timeout=5)
    if response.status_code == 200:
        return response.text


def getScraperInstanceBy(scraperName: str) -> AbstractScraper:
    for portalNameClass in AbstractScraper.__subclasses__():
        if portalNameClass.__name__ == scraperName:
            scraperInstance = portalNameClass()
            break
    return scraperInstance


@shared_task(bind=True)
def prepareScraperTask(self, scraperName: str) -> None:
    scraperInstance = getScraperInstanceBy(scraperName) # get scraper instance by name because celery can't serialize instance of this class
    searchParameters = GroupedSearchParameters().get()
    urls = scraperInstance.createUrlsFrom(searchParameters).get()

    for url in urls:
        scraperLinksTask.delay(url, scraperName)


@shared_task(bind=True)
def scraperLinksTask(self, url,  scraperName: str) -> None:
    scraperInstance = getScraperInstanceBy(scraperName) # get scraper instance by name because celery can't serialize instance of this class
    
    # for testing
    #htmlString = downloadHtml.delay(url)
    with open("scrapingApp/tests/olx-list.html", "r", encoding="utf-8") as f:
        htmlString = f.read()

    urls = scraperInstance.scrapLinks(htmlString).execute()
    
    logger.info("In scraperLinksTask: Value of scraped urls: "+ str(urls)+ "; Typ of urls"+str(type(urls))+ "; Value of scraperName" +str(scraperName))

    for url in urls:
        logger.info("In scraperLinksTask loop: Value of url: "+ str(url)+ "; Value of scraperName" +str(scraperName))
        scrapDetailsTask.delay(url, scraperName)


@shared_task(bind=True)
def scrapDetailsTask(self, url,  scraperName: str) -> None:
    logger.info("In scrapDetailsTask: Value of url: "+ str(url)+ "; Value of scraperName" +str(scraperName))
    
    scraperInstance = getScraperInstanceBy(scraperName) # get scraper instance by name because celery can't serialize instance of this class
    # for testing
    #htmlString = downloadHtml.delay(url)
    with open("scrapingApp/tests/olx-detail.html", "r", encoding="utf-8") as f:
        htmlString = f.read()

    realEstateDetails = scraperInstance.scrapDetails(htmlString).execute()
    
    saveRealEstateDetails.delay(realEstateDetails)


@shared_task(bind=True)
def startScraperTasks(self):
    i =0
    for portalNameClass in AbstractScraper.__subclasses__():
        prepareScraperTask.delay(portalNameClass.__name__)
        logger.info("Start scrap task: "+str(i) + str(portalNameClass.__name__))
