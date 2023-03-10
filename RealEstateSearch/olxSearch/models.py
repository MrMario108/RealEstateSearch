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

class HtmlTagsNameToFind(models.Model):
    # store name of html tags to find in html code

    name = models.CharField(max_length=50, default="")
    values = models.TextField(default="")
    # urlPatern = models.TextField(default="")


# review = soup.findAll("p",attrs={"data-testid"="txtDateGivenReviewFilter0"}) 
# soup.select('p[data-testid="txtDateGivenReviewFilter0"]')

# name      : olx-list
# values    : contener,listing-grid-container,advertisement,l-card,link,a

    #OLX
    # contener z listą ogłoszeń     class="listing-grid"
        # ogłoszenie na liście          data-cy="l-card"
            # link do ogłoszenia            po prostu <a link w l-card

    # OLX szczegóły ogłoszenia
    # kategoria i rodzaj transakcji  
        # znaleść <ol data-testid="breadcrumbs" data-cy="categories-breadcrumbs" class="css-jramwl">
            # znaleść ostatni link i 
            # <a href="/nieruchomosci/mieszkania/sprzedaz/warszawa/" class="css-tyi2d1">Sprzedaż - Warszawa</a>
            # lub ostatni element listy
            # <li data-testid="breadcrumb-item" class="css-7dfllt"><a href="/nieruchomosci/mieszkania/sprzedaz/warszawa/" class="css-tyi2d1">Sprzedaż - Warszawa</a></li>
                # podzielić po /
    # zdjęcie
        # znaleść <div class="swiper-zoom-container">
            # wyciągnąć src 
            # <img src="https://ireland.apollo.olxcdn.com:443/v1/files/kp9sm8yefcbv1-PL/image;s=2592x1944" alt="Mieszkanie z ogródkiem przy lesie okolice ul. Mareckiej Bezczynszowe." sizes="(min-width: 1100px) 992px, (min-width: 780px) 516px, 100vw" srcset="https://ireland.apollo.olxcdn.com:443/v1/files/kp9sm8yefcbv1-PL/image;s=389x272 420w, https://ireland.apollo.olxcdn.com:443/v1/files/kp9sm8yefcbv1-PL/image;s=516x361 780w, https://ireland.apollo.olxcdn.com:443/v1/files/kp9sm8yefcbv1-PL/image;s=1000x700 992w" data-testid="swiper-image" class="css-1bmvjcs"></div>