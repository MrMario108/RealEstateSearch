import pytest
from django.test import TestCase
from scrapingApp.utils.abstractScraper import AbstractScraper, OLXCreateUrlsFromParameters, OLXScrapLinks, OLXScrapDetails
from scrapingApp.utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City, User
from olxSearch.tests.factory import CityFactory, CategoryFactory, UserFactory, SearchingSettingsFactory
from scrapingApp.tasks import GroupedSearchParameters
from django.utils import timezone
from django.conf import settings
import os
from datetime import datetime

@pytest.mark.django_db
class FixtureDB():
    @pytest.fixture
    def category(self):
        CategoryFactory.create(categoryName="Domy")
        CategoryFactory.create(categoryName="Mieszkania")
    
    @pytest.fixture
    def city(self):
        CityFactory.create(cityName="Ruda Śląska")
        CityFactory.create(cityName="Warszawa")
    
    @pytest.fixture
    def user(self):
        UserFactory.create()
    
    @pytest.fixture
    def searchingSettings(self, city:City, category:Category, user:User):
        SearchingSettingsFactory.create(
            user = User.objects.get(username="admin"),
            city = City.objects.get(cityName="Warszawa"),
            category = Category.objects.get(categoryName="Mieszkania"),
            title= 'title',
            area=30,
            rooms=1,
            date_created = timezone.now(),
            price = 4000
        )
        SearchingSettingsFactory.create(
            user = User.objects.get(username="admin"),
            city = City.objects.get(cityName="Warszawa"),
            category = Category.objects.get(categoryName="Mieszkania"),
            title= 'title',
            area=30,
            rooms=1,
            date_created = timezone.now(),
            price = 5000
        )
        SearchingSettingsFactory.create(
            user = User.objects.get(username="admin"),
            city = City.objects.get(cityName="Ruda Śląska"),
            category = Category.objects.get(categoryName="Domy"),
            title= 'title',
            area=30,
            rooms=1,
            date_created = timezone.now(),
            price = 3000
        )
        SearchingSettingsFactory.create(
            user = User.objects.get(username="admin"),
            city = City.objects.get(cityName="Ruda Śląska"),
            category = Category.objects.get(categoryName="Domy"),
            title= 'title',
            area=30,
            rooms=1,
            date_created = timezone.now(),
            price = 2000
        )


@pytest.mark.django_db
class Test_getGroupedSearchParameters(FixtureDB):
    
    def test_SerchingSettings_len(self, searchingSettings, city, category, user):
        assert len(SearchingSettings.objects.all()) == 4

    def test_getGroupedSearchParameters_InstanceType(self, searchingSettings, city, category, user):
        assert isinstance(GroupedSearchParameters().get(), list)

    def test_getGroupedSearchParameters_len(self, searchingSettings, city, category, user):
        assert len(GroupedSearchParameters().get()) == 2  
        
    def test_getGroupedSearchParameters_WarszawaGroup(self, searchingSettings, city, category, user):
        values = GroupedSearchParameters().get()
        assert values[1]["city__slug"] == "warszawa" and values[1]["price"] == 5000 and values[1]["category__categoryName"] == "Mieszkania"

    def test_getGroupedSearchParameters_RudaGroup(self, searchingSettings, city, category, user):
        values = GroupedSearchParameters().get()
        assert values[0]["city__slug"] == "ruda-slaska" and values[0]["price"] == 3000 and values[0]["category__categoryName"] == "Domy"
    

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