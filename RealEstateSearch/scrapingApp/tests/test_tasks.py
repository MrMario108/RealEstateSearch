import pytest
from olxSearch.models import SearchingSettings, Category, City, User
from olxSearch.tests.factory import CityFactory, CategoryFactory, UserFactory, SearchingSettingsFactory
from scrapingApp.tasks import GroupedSearchParameters
from django.utils import timezone

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

