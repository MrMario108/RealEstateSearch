from datetime import timedelta

from django.utils import timezone
from factory import LazyAttribute, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import date_time, internet, python, address
from olxSearch.models import City, Category, SearchingSettings
from django.contrib.auth.models import User
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

class SearchingSettingsFactory(DjangoModelFactory):
    class Meta:
        model = SearchingSettings
    
    title = "title"
    price = 4000
    area = 30
    category = SubFactory(CategoryFactory)
    rooms = 1
    city = SubFactory(CityFactory)
    date_created = timezone.now()
    user = SubFactory(User)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = "admin"
    password = "Polmrok0"
    email = "m.majewski108@gmail.com"

# 'Warszawa', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Białystok', 'Katowice', 'Gdynia', 'Częstochowa', 'Radom', 'Rzeszów', 'Toruń', 'Sosnowiec', 'Kielce', 'Gliwice', 'Olsztyn', 'Zabrze', 'Bielsko-Biała', 'Bytom', 'Zielona Góra', 'Rybnik', 'Ruda Śląska', 'Opole', 'Tychy', 'Świętochłowice', 'Chorzów' 