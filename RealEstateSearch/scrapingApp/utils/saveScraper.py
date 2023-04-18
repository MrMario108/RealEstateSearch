from olxSearch import models
from datetime import datetime


class SaveApartment():
    def __init__(self, status, scrapedDetails) -> None:
        self.isExists = status
        self.scrapedDetails = scrapedDetails

    
    @classmethod
    def checkIfExists(cls,scrapedDetails):
        """Check through 4 params is scrapedDetails is in db """        
        findedApartment = []
        findedApartment = models.Apartment.objects.filter(advId=scrapedDetails["advId"] , category__categoryName=scrapedDetails["category"], city__cityName=scrapedDetails["city"], rooms=scrapedDetails["rooms"])
        
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
            newApartment.city = models.City.objects.get(cityName=scrapedDetails["city"])
            newApartment.category = models.Category.objects.get(categoryName=scrapedDetails["category"])
            newApartment.buildingType = models.BuildingType.objects.get(name = scrapedDetails["buildingType"])
            newApartment.advId = scrapedDetails["advId"]
            newApartment.title = scrapedDetails["title"]
            newApartment.pic = scrapedDetails["pic"]
            newApartment.price = scrapedDetails["price"]
            newApartment.area = scrapedDetails["area"]
            newApartment.rooms = scrapedDetails["rooms"]
            newApartment.date_published = scrapedDetails["date_published"]
            newApartment.link = scrapedDetails["link"]
            newApartment.save()
        return True

    def delCategory(self):
        pass
        #models.Category.objects.all().delete()
        
        
