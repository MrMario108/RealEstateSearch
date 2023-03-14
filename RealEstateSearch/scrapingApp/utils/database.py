from olxSearch import models
from datetime import datetime


class Database():
    def __init__(self, status,scrapedDetails) -> None:
        self.isExists = status
        self.scrapedDetails = scrapedDetails

    
    @classmethod
    def checkIfExists(cls,scrapedDetails):
        """Check through 5 params is scrapedDetails is in db """        
        findedApartment = []
        print('Class: Database; method: checkIfExists; scrapedDetails =', scrapedDetails, file=open("log.txt", "a"))
        findedApartment = models.Apartment.objects.filter(advId=scrapedDetails["advId"] , category__categoryName=scrapedDetails["category"], city__cityName=scrapedDetails["city"], rooms=scrapedDetails["rooms"], area=scrapedDetails["area"])
        print('Class: Database; method: checkIfExists; findedApartment =', findedApartment, file=open("log.txt", "a"))
        
        if len(findedApartment) !=0:
            print('Class: Database; method: checkIfExists; len - findedApartment =', len(findedApartment), file=open("log.txt", "a"))

            return cls(True, scrapedDetails)
        else:
            return cls(False, scrapedDetails)    

    def execute(self):
        if self.isExists:
            pass
        else:
            scrapedDetails = self.scrapedDetails
            newApartment = models.Apartment()
            newApartment.advId = scrapedDetails["advId"]
            newApartment.link = scrapedDetails["link"]
            newApartment.pic = scrapedDetails["pic"]
            newApartment.title = scrapedDetails["title"]
            newApartment.price = scrapedDetails["price"]
            newApartment.date_published = scrapedDetails["date_published"]
            newApartment.area = scrapedDetails["area"]
            newApartment.category = models.Category.objects.get(categoryName=scrapedDetails["category"])
            newApartment.rooms = scrapedDetails["rooms"]
            newApartment.city = models.City.objects.get(cityName=scrapedDetails["city"])
            newApartment.save()

    def delCategory(self):
        pass
        #models.Category.objects.all().delete()
        
        
