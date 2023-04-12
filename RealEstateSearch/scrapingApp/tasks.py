from celery import shared_task

from .utils.abstractScraper import AbstractScraper
from .utils.saveScraper import SaveApartment
from olxSearch.models import SearchingSettings, Category, City
from django.db.models import Max
from django.utils import settings

logger = logging.getLogger('celeryLogger')

class GroupedSearchParameters():
    
    def get(self) -> list:
        """ Groups parameters to limit the number of web pages scraped and the number of properties found """
        groupedSearchParameters = []
        category = Category.objects.all()
        cities = City.objects.all()
        
        for cat in category:
            for city in cities:
                finded = self.findMaxPrice(cat, city)
                if finded != None:
                    groupedSearchParameters.append(finded)

        logger.info("getGroupedSearchParameters; returned values: "+ str(groupedSearchParameters))

        return groupedSearchParameters

    def joinSingleSearchParametersFrom(self, selectedParameters, maxPrice):

        selectedParameters[0]["price"] = maxPrice['price__max']
        logger.info("joinSingleSearchParametersFrom: " + str(selectedParameters[0]))
        return selectedParameters[0]

    def findPricesForCategoryAndCity(self, category, city):
        return SearchingSettings.objects.filter(category__categoryName = category.categoryName, city__slug = city.slug).values('area', 'rooms', 'price', 'city__slug', 'category__categoryName')

    def findMaxPrice(self, category, city):
        selectedParameters = self.findPricesForCategoryAndCity(category, city)
        logger.info("getGroupedSearchParameters; selectedParameters: " + str(selectedParameters))
        maxPrice = selectedParameters.aggregate(Max('price'))
        logger.info("getGroupedSearchParameters; maxPrice: " + str(maxPrice))
        if (maxPrice['price__max'] != None):
            return self.joinSingleSearchParametersFrom(list(selectedParameters), maxPrice)


@shared_task(bind=True)
def send_mail_func(self, data = None):
    users = get_user_model().objects.all()
    for user in users:
        print(user.email)
        mail_subject = 'Hi! Celery testing'
        message = 'data scedule from RealEstateSearch'
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email= local.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False
        )
    return "Done"