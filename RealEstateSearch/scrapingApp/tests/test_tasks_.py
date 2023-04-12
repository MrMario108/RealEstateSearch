import pytest
from django.test import TestCase
from scrapingApp.utils.abstractScraper import AbstractScraper, OLXCreateUrlsFromParameters
from scrapingApp.utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City, User
from scrapingApp.tasks import GroupedSearchParameters
from django.utils import timezone
from django.utils.text import slugify

@pytest.fixture
def make_category(db):
    def make(
        categoryName: str = "Mieszkania",
    ):
        category = Category(
            categoryName=categoryName
        )
        return category

    return make

@pytest.fixture
def make_city():
    def make(
        cityName: str = "Warszawa",
        slug: str = "warszawa"
    ):
        city = City(
            cityName=cityName, slug=slugify(cityName)
        )
        return city

    return make

@pytest.fixture
def make_user():
    def make(
        username: str = "admin",
        password: str = "Polmrok0",
        email: str = "test@example.com",
        **rest
    ):
        user = User(
            username=username, password=password, email=email, **rest
        )
        return user

    return make

@pytest.fixture
def make_searchingSettings(make_user, make_city, make_category):
    def make(title, category=None, user=None, city=None):
        if user is None:
            user = make_user()
        if city is None:
            city = make_city()
        if category is None:
            category = make_category()
        
        searchingSettings = SearchingSettings(
            user=user,
            city=city,
            category=category,
            title= title,
            area=30,
            rooms=1,
            date_created = timezone.now(),
            price = 4000
        )
        return searchingSettings

    return make

def test_searchingSettings(make_searchingSettings):
    searchingSettings_1 = make_searchingSettings(title="Elaine")
    assert searchingSettings_1.title == "Elaine"

def test_searchingSettings_2(make_searchingSettings, make_category):
    category = make_category(categoryName="Domy")
    searchingSettings_1 = make_searchingSettings(title="Elaine", category = category)
    assert searchingSettings_1.category.categoryName == "Domy"

#def test_findMaxPrice(make_category):
#    make_category(categoryName="Domy")
#    make_category(categoryName="Działki")
#    make_category(categoryName="Mieszkania")
#    assert "Mieszkania" in Category.objects.all()


#@pytest.fixture
#def city(db):
#    cities = ('Warszawa', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Białystok', 'Katowice', 'Gdynia', 'Częstochowa', 'Radom', 'Rzeszów', 'Toruń', 'Sosnowiec', 'Kielce', 'Gliwice', 'Olsztyn', 'Zabrze', 'Bielsko-Biała', 'Bytom', 'Zielona Góra', 'Rybnik', 'Ruda Śląska', 'Opole', 'Tychy', 'Świętochłowice', 'Chorzów' )
#    for city in cities:
#        CityFactory.create(cityName=city)