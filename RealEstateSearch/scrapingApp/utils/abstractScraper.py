from __future__ import annotations
from abc import ABC, abstractmethod
import slugify
from bs4 import BeautifulSoup
import logging
from olxSearch.models import City, Apartment, Category
from datetime import datetime

logger = logging.getLogger('django')

class AbstractScraper(ABC):

    @abstractmethod
    def scrapLinks(self, htmlString) -> AbstractsSrapLinks:
        pass

    @abstractmethod
    def scrapDetails(self, htmlString) -> AbstractsSrapDetails:
        pass

    @abstractmethod
    def createUrlsFrom(self, searchParameters) -> AbstractsCreateUrlsFromParameters:
        pass

class OLX_Scraper(AbstractScraper):

    def scrapLinks(self, htmlString) -> AbstractsSrapLinks:
        return OLXSrapLinks(htmlString)

    def scrapDetails(self, htmlString) -> AbstractsSrapDetails:
        return OLXSrapDetails(htmlString)
    
    def createUrlsFrom(self, searchParameters) -> AbstractsCreateUrlsFromParameters:
        return OLXCreateUrlsFromParameters(searchParameters)

#class OtoDom_Scraper(AbstractScraper):
#
#    def scrapLinks(self, htmlString) -> AbstractsSrapLinks:
#        return OtoDomSrapLinks(htmlString)
#
#    def scrapDetails(self, htmlString) -> AbstractsSrapDetails:
#        return OtoDomSrapDetails(htmlString)
#
#    def createUrlsFrom(self, searchParameters) -> AbstractsCreateUrlsFromParameters:
#        return OtoDomCreateUrlsFromParameters(searchParameters)


class AbstractsSrapLinks(ABC):
    @abstractmethod
    def __init__(self, htmlString):
        pass

    @abstractmethod
    def execute(self) -> list:
        pass

class AbstractsCreateUrlsFromParameters(ABC):
    @ abstractmethod
    def __init__(self, searchParameters):
        pass
    
    @abstractmethod
    def createUrls(self) -> None:
        pass

    @abstractmethod
    def get(self) -> list:
        pass

class AbstractsSrapDetails(ABC):
    @abstractmethod
    def __init__(self, htmlString):
        pass

    @abstractmethod
    def execute(self) -> None:
        pass


class OLXSrapLinks(AbstractsSrapLinks):
    def __init__(self, htmlString):
        self.htmlString = htmlString

    def correctUrls(self, links):
        correctedLinks = []
        for link in links:
            if not 'https://www.otodom.pl/pl/oferta' in link:
                if not "/d/oferta" in link:
                    if not "/d/nieruchomosci" in link:
                        logger.error('Class: OLXSrapLinks; method: corectLinks; Unrecognised link =', link)
                        return False
            if not "https" in link:
                link = "https://www.olx.pl" + link

            correctedLinks.append(link)
        return correctedLinks

    def scrapAdvsUrls(self, advertisements):
        urls = []
        for adv in advertisements:
            urls.append(adv.a["href"])
        return urls

    def getLinks(self, advertisements):
        urlsToCorrect = self.scrapAdvsUrls(advertisements)
        urls = self.correctUrls(urlsToCorrect)
        return urls

    @classmethod
    def execute(self) -> list:
        soup = BeautifulSoup(self.htmlString, "html.parser")
        gridWithListOfAds = soup.body.find("div", {"data-testid":"listing-grid"})
        advertisements = gridWithListOfAds.find_all(attrs={"data-cy":"l-card"})
        links = self.getLinks(advertisements)
        return links


class OLXSrapDetails(AbstractsSrapDetails):
    def __init__(self, htmlString):
        self.htmlString = htmlString

    def execute(self) -> str:
        return "OLXSrapedDetails."
    
    def categoryAndCity(self, soup):
        categoriesAndCity = {}
        scrapedGroupWithCategories = soup.body.find_all("li", {"data-testid":"breadcrumb-item"})
        categoryAndCity = [i.find("a").text for i in scrapedGroupWithCategories]

        categoriesAndCity["advCategory"] = categoryAndCity[0].strip()
        categoriesAndCity["category"] = categoryAndCity[1].strip()
        categoriesAndCity["city"] = categoryAndCity[5].split("-")[-1].strip()

        return categoriesAndCity

    def checkIsRequestedAdv(self, categoriesAndCity):
        if "Nieruchomości" != categoriesAndCity["advCategory"]:
            return False
        elif not categoriesAndCity["city"] in City.objects.all().values_list("cityName", flat=True):
            return False
        else:
            return True

    def informationGroup(self, soup):
        scrapedDetails = {}
        informationGroupTemp = soup.body.find_all("li",{"class":"css-1r0si1e"})
        informationGroupList = [i.find("p").text for i in informationGroupTemp]
        
        # informationGroupList has variable len and places can are mixed
        # ['Prywatne', 'Cena za m²: 76.74 zł/m²', 'Poziom: 9', 'Umeblowane: Tak', 'Rynek: Pierwotny', 'Rodzaj zabudowy: Apartamentowiec', 'Powierzchnia: 43 m²', 'Liczba pokoi: 2 pokoje']
        for informationGroup in informationGroupList:   
            informations = informationGroup.split()

            if informations[0] == "Prywatne" or informations[0] == "Prywatne":
                scrapedDetails["ownerCategory"] = informations[0]
            if informations[0] == "Poziom:":
                scrapedDetails["level"] = informations[1]
            if informations[0] == "Rynek:":
                scrapedDetails["market"] = informations[1]
            if informations[0] == "Rodzaj":
                scrapedDetails["buildingType"] = informations[2]
            if informations[0] == "Powierzchnia:":
                area = informations[1]
                try:
                    scrapedDetails["area"] = float(area.replace(',','.'))
                except:
                    scrapedDetails["area"] = None
            if informations[0] == "Liczba":
                scrapedDetails["rooms"] = informations[2]
        return scrapedDetails
    
    def price(self, soup):
        priceTemp = soup.body.find("div",{"data-testid":"ad-price-container"}).find("h3").strings
        priceTemp = [i for i in priceTemp]
        try:
            price = int(priceTemp[0].strip().replace(' ',''))
        except:
            price = None
        
        return price
    
    def changeMonth(self, month):
        match month:
            case "styczeń":
                return "01"
            case "luty":
                return "02"
            case "marzec":
                return "03"
            case "kwiecień":
                return "04"
            case "maj":
                return "05"
            case "czerwiec":
                return "06"
            case "lipiec":
                return "07"
            case "sierpień":
                return "08"
            case "wrzesień":
                return "09"
            case "październik":
                return "10"
            case "listopad":
                return "11"
            case "grudzień":
                return "12"
            case _:
                return "01"
    
    def formatDate(self, date):
        """Input data: "1 stycznia 2023" Output data: datatime: 01-01-2023"""

        date = date.split(" " or "-")
        date[1] = self.changeMonth(date[1].lower())
        try:
            date = datetime.strptime(date[0]+"-"+date[1]+"-"+date[2], "%d-%m-%Y")
        except:
            date = datetime.now()
        return date
    def scrapDetails(self):
        """Method with sets of complex methods to scrape all data from sell advertisement"""
        """not all advs have all params also her are some params that are not in database model
        for add to database model in the future"""
        scrapedDetails = {}
        soup = BeautifulSoup(self.htmlString, "html.parser")
        
        categoriesAndCity = categoriesAndCity(soup)

        if not self.checkIsRequestedAdv(categoriesAndCity):
            return False
        
        scrapedDetails["category"] = categoriesAndCity["category"]
        scrapedDetails["city"] = categoriesAndCity["city"]
        
        pictureUrl = soup.body.find(class_="swiper-zoom-container")
        scrapedDetails["pic"] = pictureUrl.find("img")["src"]
        
        date_published = soup.body.find("span",{"data-cy":"ad-posted-at"}).string
        scrapedDetails["date_published"] = self.formatDate(date_published)

        scrapedDetails["title"] = soup.body.find("h1",{"data-cy":"ad_title"}).string
        scrapedDetails["price"] = self.price(soup)

        informations = self.informationGroup(soup)
        scrapedDetails["ownerCategory"] = informations["ownerCategory"]
        scrapedDetails["level"] = informations["level"]
        scrapedDetails["market"] = informations["market"]
        scrapedDetails["buildingType"] = informations["buildingType"]
        scrapedDetails["area"] = informations["area"]
        scrapedDetails["rooms"] = informations["rooms"]
            
        scrapedDetails["description"] = soup.body.find("div",{"data-cy":"ad-description"})
        id = soup.body.find("div",{"data-cy":"ad-footer-bar-section"}).find("span").strings
        scrapedDetails["advId"] = [i for i in id if len(i) > 4]
        
        return scrapedDetails

    
    
class OLXCreateUrlsFromParameters(AbstractsCreateUrlsFromParameters):
    def __init__(self, searchParameters):
        self.searchParameters = searchParameters
        self.urlsList = []
        self.createUrls()

    def createUrls(self) -> None:
        """Create requests from search parameters"""
        roomsDict = {
            1 : "one",
            2 : "two",
            3 : "three",
            4 : "four",
            5 : "five",
            6 : "six",
            7 : "seven",
            8 : "eight",
            9 : "nine",
            0 : ""
        }
        for param in self.searchParameters:
            print("OLXCreateUrlsFromParameters; searchParameters =",self.searchParameters)
            #url = f"""https://www.olx.pl/d/nieruchomosci/{param.category}/sprzedaz/{slugify(param.city)}/?search%5Bfilter_enum_rooms%5D%5B0%5D={roomsDict[param.rooms]}&search%5Bfilter_float_price_per_m:to%5D={param.price}""".lower()
            #self.urlsList.append(url)

    def get(self) -> list:
        return self.urlsList




#
#class OtoDomSrapLinks(AbstractsSrapLinks):
#    def __init__(self, htmlString):
#        self.htmlString = htmlString
#
#    def execute(self) -> str:
#        return ["http://onet.pl",]
#
#
#class OtoDomSrapDetails(AbstractsSrapDetails):
#    def __init__(self, htmlString):
#        self.htmlString = htmlString
#
#    def execute(self) -> str:
#        return "OtoDomSrapedDetails"
#
#
#class OtoDomCreateUrlsFromParameters(AbstractsCreateUrlsFromParameters):
#    def __init__(self, searchParameters):
#        self.searchParameters = searchParameters
#        self.urlsList = []
#        self.createUrls()
#
#    def createUrls(self) -> None:
#        """Create requests from search parameters"""
#        roomsDict = {
#            1 : "one",
#            2 : "two",
#            3 : "three",
#            4 : "four",
#            5 : "five",
#            6 : "six",
#            7 : "seven",
#            8 : "eight",
#            9 : "nine",
#            0 : ""
#        }
#        for param in self.searchParameters:
#            self.urlsList.append(f"""https://www.otodom.pl/""".lower())
#   
#    def get(self) -> list:
#        return self.urlsList
#