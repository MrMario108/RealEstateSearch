from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class City(models.Model):
    slug = models.SlugField(max_length=100, default="")
    cityName = models.CharField(max_length=100, default="")

    def __str__(self) -> str:
        return self.cityName


class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.categoryName


class RealEstate(models.Model):
    advId = models.IntegerField(default=0)
    link = models.CharField(max_length=200, default="#")
    pic = models.CharField(max_length=300, default="")
    title = models.CharField(max_length=100, default="")
    price = models.FloatField(default=0.0)
    # date_published = models.DateField('date published')
    date_published = models.CharField(max_length=50, default="")
    area = models.FloatField(default=0.0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='realEstateCategory')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='realEstateCity')

    class Meta:
        abstract = True


class Apartment(RealEstate):

    rooms = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return 'User profile {}.'.format(self.user.username)


class SearchingSettings(models.Model):
    title = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='searchingSettingCategory')
    rooms = models.IntegerField(default=0, blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='searchingSettingCity')
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
