import pytest
from django.test import TestCase
from utils.abstractScraper import AbstractScraper
from utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max
from tasks import getGroupedSearchParameters

@pytest.fixture
def data():
    return "jakieś dane"

def test_getGroupedSearchParameters() -> None:
    
    assert type(getGroupedSearchParameters()) == type(list)


class CarModuleTestCase(TestCase):
    
    def test_getGroupedSearchParameters(self): # names with test_ are run automatically and its unit test
        self.assertEqual(type(getGroupedSearchParameters()), type(list))
    
    # this method is called after each test - it's a good place to clean up - beck all changes made to the database
    def tearDown(self) -> None: 
        return super().tearDown()