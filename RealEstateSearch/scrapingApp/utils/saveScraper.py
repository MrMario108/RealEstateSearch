from olxSearch import models
from datetime import datetime


class SaveApartment():
    def __init__(self, status,scrapedDetails) -> None:
        self.isExists = status
        self.scrapedDetails = scrapedDetails

    
    @classmethod
    def checkIfExists(cls,scrapedDetails):
        """Check through 5 params is scrapedDetails is in db """        
        findedApartment = []
        findedApartment = models.Apartment.objects.filter(advId=scrapedDetails["advId"] , category__categoryName=scrapedDetails["category"], city__cityName=scrapedDetails["city"], rooms=scrapedDetails["rooms"], area=scrapedDetails["area"])
        
        if len(findedApartment) !=0:
            return cls(True, scrapedDetails)
        else:
            return cls(False, scrapedDetails)    

    def tryToSave(self):
        if self.isExists:
            raise Exception("Apartment already exists")
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
        
        
