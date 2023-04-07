from datetime import timedelta

from django.utils import timezone
from factory import LazyAttribute, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import date_time, internet, python, address
from olxSearch.models import City, Category
from django.utils.text import slugify
import random

faker = Faker()
faker.add_provider(internet)
faker.add_provider(date_time)
faker.add_provider(python)
faker.add_provider(address)

class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    cityName = LazyFunction(lambda: faker.city())
    slug = LazyAttribute(lambda instance: slugify(str(instance.cityName)))

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    categoryName = LazyFunction(lambda: random.sample(("Mieszkania", "Domy", "Działki"),1)[0])