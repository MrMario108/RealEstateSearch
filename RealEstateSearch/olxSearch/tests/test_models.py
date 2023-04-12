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
        assert str(city) == f"{city.cityName}"
    
    def test_instance_city(self, city):
        assert isinstance(city.cityName, str)
        assert isinstance(city.slug, str)

    def test_slug_city(self, city):
        assert city.slug == slugify(city.cityName)






# docker exec -it realestatesearch-web-1 pytest -v 
# docker exec -it realestatesearch-web-1 pytest -v --create-db  # utworzy od nowa bazę testową
# docker exec -it realestatesearch-web-1 pytest --cov=olxSearch --cov-report=html