<<<<<<< HEAD
=======
<<<<<<< HEAD
from celery import shared_task

from .utils.abstractScraper import AbstractScraper
from .utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max
from django.utils import settings

logger = logging.getLogger('celeryLogger')

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
=======
>>>>>>> 1bc5f64 (added-first-tests)
import logging

import requests
from celery import shared_task

from .utils.abstractScraper import AbstractScraper
from .utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max

logger = logging.getLogger('celeryLogger')

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

<<<<<<< HEAD
=======

@shared_task(bind=True)
>>>>>>> 1bc5f64 (added-first-tests)
def saveRealEstateDetails(self, realEstateDetails):
    SaveApartment.checkIfExists(realEstateDetails).tryToSave()


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
        logger.info("Start scrap task: "+str(i) + str(portalNameClass.__name__))
<<<<<<< HEAD
        prepareScraperTask.delay(portalNameClass.__name__)
=======
        prepareScraperTask.delay(portalNameClass.__name__)
>>>>>>> aae4168 (added-first-tests)
>>>>>>> 1bc5f64 (added-first-tests)
