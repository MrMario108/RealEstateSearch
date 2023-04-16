import pytest
from scrapingApp.utils.abstractScraper import OLXCreateUrlsFromParameters, OLXScrapLinks, OLXScrapDetails
from django.conf import settings
import os
from datetime import datetime


class Test_OLXCreateUrlsFromParameters():
    
    @pytest.fixture
    def searchParameters(self):
        searchParameters = []
        searchParameters.append({'area': 30, 'rooms': 1, 'price': 4000, 'city__slug': 'ruda-slaska', 'category__categoryName': 'Mieszkania'})
        searchParameters.append({'area': 30, 'rooms': 1, 'price': 4000, 'city__slug': 'Ruda Śląska', 'category__categoryName': 'Mieszkania'})
        searchParameters.append({'area': 30, 'rooms': 11, 'price': 4000, 'city__slug': 'ruda-slaska', 'category__categoryName': 'Mieszkania'})

        return searchParameters
    
    @pytest.fixture
    def requiredOutput(self):
        return "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/ruda-slaska/?search%5Bfilter_float_m:to%5D=30&search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Bfilter_float_price_per_m:to%5D=4000"
    
    @pytest.fixture
    def requiredOutput_Room9(self):
        return "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/ruda-slaska/?search%5Bfilter_float_m:to%5D=30&search%5Bfilter_enum_rooms%5D%5B0%5D=nine&search%5Bfilter_float_price_per_m:to%5D=4000"

    def test_OLXCreateUrlsFromParameters_CheckType(self, searchParameters):
        assert isinstance(OLXCreateUrlsFromParameters(searchParameters).get(), list)

    def test_OLXCreateUrlsFromParameters_GoodData(self, searchParameters, requiredOutput):
        assert OLXCreateUrlsFromParameters(searchParameters).get()[0] == requiredOutput
    
    def test_OLXCreateUrlsFromParameters_WithBadInputCityName(self, searchParameters, requiredOutput):
        assert OLXCreateUrlsFromParameters(searchParameters).get()[1] == requiredOutput
    
    def test_OLXCreateUrlsFromParameters_WithBadInputRooms(self, searchParameters, requiredOutput_Room9):
        assert OLXCreateUrlsFromParameters(searchParameters).get()[2] == requiredOutput_Room9

for portalNameClass in AbstractScraper.__subclasses__():
        if portalNameClass.__name__ == scraperName:
            scraperInstance = portalNameClass()
   
class Test_OLXScrapLinks():
    @pytest.fixture
    def htmlString(self):
        with open(os.path.join(settings.BASE_DIR, "scrapingApp/tests/olx-list.html"), "r", encoding="utf-8") as f:
            htmlString = f.read()
        return htmlString
    
    def test_OLXScrapLinks_CheckType(self, htmlString):
        assert isinstance(OLXScrapLinks(htmlString).execute(), list)
        
    def test_OLXScrapLinks_CheckNumberOfScrapedLinks(self, htmlString):
        assert len(OLXScrapLinks(htmlString).execute()) == 7


class Test_OLXScrapDetails():
    @pytest.fixture
    def htmlString(self):
        with open(os.path.join(settings.BASE_DIR, "scrapingApp/tests/olx-detail.html"), "r", encoding="utf-8") as f:
            htmlString = f.read()
        return htmlString
    
    @pytest.fixture
    def scrapedDetails(self, htmlString):
        return OLXScrapDetails(htmlString).execute()
    
    @pytest.fixture
    def outputScrapedDetails(self):
        outputScrapedDetails = {}
        outputScrapedDetails["category"] = "Mieszkania"
        outputScrapedDetails["city"] = "Warszawa"
        outputScrapedDetails["pic"] = "https://ireland.apollo.olxcdn.com:443/v1/files/wfmstc0ksgm5-PL/image;s=1000x667"
        outputScrapedDetails["date_published"] = datetime.strptime("07-03-2023", "%d-%m-%Y")
        outputScrapedDetails["title"] = "Odstąpię p"
        outputScrapedDetails["price"] = 228000
        outputScrapedDetails["ownerCategory"] = "Prywatne"
        outputScrapedDetails["level"] = '6'
        outputScrapedDetails["market"] = "Wtórny"
        outputScrapedDetails["buildingType"] = "Blok"
        outputScrapedDetails["area"] = 44,50
        outputScrapedDetails["rooms"] = 2
        outputScrapedDetails["description"] = "Odsprzedam"
        outputScrapedDetails["advId"] = '809200371'

        return outputScrapedDetails

    def test_CheckType(self, scrapedDetails):
        assert isinstance(scrapedDetails, dict)

    def test_checkCategory(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["category"] == outputScrapedDetails["category"]

    def test_checkCity(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["city"] == outputScrapedDetails["city"]

    def test_checkPic(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["pic"] == outputScrapedDetails["pic"]

    def test_checkDate(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["date_published"] == outputScrapedDetails["date_published"]

    def test_checkTitle(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["title"][:10] == outputScrapedDetails["title"][:10]

    def test_checkPrice(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["price"] == outputScrapedDetails["price"]

    def test_checkOwnerCategory(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["ownerCategory"] == outputScrapedDetails["ownerCategory"]

    def test_checkLevel(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["level"] == outputScrapedDetails["level"]
    
    def test_checkMarket(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["market"] == outputScrapedDetails["market"]

    def test_checkBuildingType(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["buildingType"] == outputScrapedDetails["buildingType"]

    def test_checkArea(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["area"] == outputScrapedDetails["area"]

    def test_checkRooms(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["rooms"] == outputScrapedDetails["rooms"]
    
    def test_checkDescription(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["description"][:10] == outputScrapedDetails["description"][:10]
    
    def test_checkArea(self, scrapedDetails, outputScrapedDetails):
        assert scrapedDetails["advId"] == outputScrapedDetails["advId"]