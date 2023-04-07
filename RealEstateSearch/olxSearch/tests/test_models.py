from django.test import TestCase

import pytest
from django.utils.text import slugify
from olxSearch.models import SearchingSettings, Category, City, User
from olxSearch.tests.factory import CityFactory, CategoryFactory

@pytest.mark.django_db
class TestCity:
    @pytest.fixture
    def city(self):
        return CityFactory.create()
    
    def test_str_city(self, city):
        print(str(city), f"{city.cityName}")
        assert str(city) == f"{city.cityName}"
    
    def test_instance_city(self, city):
        assert isinstance(city.cityName, str)
        assert isinstance(city.slug, str)

    def test_slug_city(self, city):
        print(city.slug)
        assert city.slug == slugify(city.cityName)


@pytest.mark.django_db
class TestCategory:
    @pytest.fixture
    def category(self):
        return CategoryFactory.create()
    
    def test_str_category(self, category):
        assert str(category) == f"{category.categoryName}"
    
    def test_instance_category(self, category):
        assert isinstance(category.categoryName, str)

    def test_value_category(self, category):
        assert category.categoryName in ("Mieszkania", "Domy", "Działki")



# docker exec -it realestatesearch-web-1 pytest -v
# docker exec -it realestatesearch-web-1 pytest --cov=olxSearch --cov-report=html