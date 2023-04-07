#import pytest
from django.test import TestCase
from scrapingApp.utils.abstractScraper import AbstractScraper, OLXCreateUrlsFromParameters
from scrapingApp.utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City, User
from scrapingApp.tasks import getGroupedSearchParameters, joinSingleSearchParametersFrom

#@pytest.fixture
def data():
    return "jakieś dane"

class FillTestDBByDefaultValues():

    def __init__(self):
        newUser = User.objects.create_user(username='admin', password='test')
        newUser.save()

        newCity = City()
        newCity.cityName = "Ruda Śląska"
        newCity.slug = "ruda_slaska"
        newCity.save()

        newCategory = Category()
        newCategory.categoryName = "Mieszkania"
        newCategory.save()

        newSearchingSettings = SearchingSettings()
        newSearchingSettings.area = 30
        newSearchingSettings.rooms = 1
        newSearchingSettings.price = 5000
        newSearchingSettings.city = City.objects.get(cityName = "Ruda Śląska")
        newSearchingSettings.category = Category.objects.get(categoryName = "Mieszkania")
        newSearchingSettings.user = User.objects.get(username = "admin")
        newSearchingSettings.save()

        newSearchingSettings = SearchingSettings()
        newSearchingSettings.area = 30
        newSearchingSettings.rooms = 1
        newSearchingSettings.price = 3000
        newSearchingSettings.city = City.objects.get(cityName = "Ruda Śląska")
        newSearchingSettings.category = Category.objects.get(categoryName = "Mieszkania")
        newSearchingSettings.user = User.objects.get(username = "admin")
        newSearchingSettings.save()


defaultSearchParametersList = [{'area': 30, 'rooms': 1, 'price': 5000, 'city__slug': 'ruda_slaska', 'category__categoryName': 'Mieszkania'}]
OLX_URLS_LIST = ['https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/ruda-slaska/?search%5Bfilter_float_m:to%5D=30&search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Bfilter_float_price_per_m:to%5D=5000']

class GetGroupedSearchParametersTestCase(TestCase):

   
    def testOutputType(self): # names with test_ are run automatically and its unit test
        self.assertEqual(type(getGroupedSearchParameters()), list)

    def testOutputValue(self):
        FillTestDBByDefaultValues()
        self.assertEqual(getGroupedSearchParameters(), defaultSearchParametersList)
        
#    def tearDown(self) -> None: 
#        return super().tearDown()
    
class OLXCreateUrlsFromParametersTestCase(TestCase):

    def testOutputType(self):
        self.assertEqual(type(OLXCreateUrlsFromParameters(defaultSearchParametersList).get()), list)

    def testOutputValue(self):
        self.assertEqual(OLXCreateUrlsFromParameters(defaultSearchParametersList).get(), OLX_URLS_LIST)

    def testPrintValue(self):
        print(OLXCreateUrlsFromParameters(defaultSearchParametersList).get())