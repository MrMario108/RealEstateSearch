import logging

import requests
from celery import shared_task

from .utils.abstractScraper import AbstractScraper
from .utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max

logger = logging.getLogger('celeryLogger')


def getGroupedSearchParameters() -> list:
    """ Groups parameters to limit the number of web pages scraped and the number of properties found """

    category = Category.objects.all()
    city = City.objects.all()
    groupedSearchParameters = []
    for cat in category:
        for cit in city:
                selectedParameters = SearchingSettings.objects.filter(category__categoryName = cat.categoryName, city__cityName = cit.cityName).values('area', 'rooms', 'price', 'city__cityName', 'category')
                logger.info("getGroupedSearchParameters; selectedParameters: " + str(selectedParameters))
                maxPrice = selectedParameters.aggregate(Max('price'))
                logger.info("getGroupedSearchParameters; maxPrice: " + str(maxPrice))
                if (maxPrice['price__max'] != None):
                    singleSearchParameter = createSingleSearchParametersFrom(list(selectedParameters), maxPrice)
                    groupedSearchParameters.append(singleSearchParameter)
    
    logger.info("getGroupedSearchParameters; : ")
    
    return groupedSearchParameters

def createSingleSearchParametersFrom(selectedParameters, maxPrice):
    """ Creates a single set of parameters from a group of parameters """
    selectedParameters[0]["price"] = maxPrice['price__max']
    #selectedParameters[0]["city"] = selectedParameters[0]["city_id"]
    return selectedParameters[0]

@shared_task(bind=True)
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
    logger.info("In prepareScraperTask: Value of scraperName: "+ str(scraperName))
    scraperInstance = getScraperInstanceBy(scraperName) # get scraper instance by name because celery can't serialize instance of this class
    logger.info("In prepareScraperTask: after getInstance")
    searchParameters = getGroupedSearchParameters()
    logger.info("In prepareScraperTask: after searchParameters" + str(searchParameters))

    print("prepareScraperTask; searchParameters: " + str(searchParameters))
    urls = scraperInstance.createUrlsFrom(searchParameters).get()

    for url in urls:
        logger.info("In prepareScraper loop: Type of urls: ; Type of scraperName")
        scraperLinksTask.delay(url, scraperName)


@shared_task(bind=True)
def scraperLinksTask(self, url,  scraperName: str) -> None:
    scraperInstance = getScraperInstanceBy(scraperName) # get scraper instance by name because celery can't serialize instance of this class
    
    # for testing
    #htmlString = downloadHtml.delay(url)
    with open("olx-list.html", "r", encoding="utf-8") as f:
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
    with open("olx-detail.html", "r", encoding="utf-8") as f:
        htmlString = f.read()

    realEstateDetails = scraperInstance.scrapDetails(htmlString).execute()
    
    saveRealEstateDetails.delay(realEstateDetails)


@shared_task(bind=True)
def startScraperTasks(self):
    i =0
    for portalNameClass in AbstractScraper.__subclasses__():
        logger.info("Start scrap task: "+str(i) + str(portalNameClass.__name__))
        prepareScraperTask.delay(portalNameClass.__name__)