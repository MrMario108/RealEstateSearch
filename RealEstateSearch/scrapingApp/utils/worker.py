from olxSearch.models import SearchingSettings
from .scraper import Scraper


class Worker():
    def __init__(self, portalName) -> None:
        self.portalName = portalName

    @classmethod
    def getSearchParameters(self):
        """get search parameters from model database"""
        allSearchParameters = SearchingSettings.objects.all()
        if allSearchParameters.count != 0:
            return allSearchParameters
        else:
            raise ValueError("No search parameters in database")

    def execute(self, allSearchParameters):
        """Create requests from search parameters"""
        # for toDo: sorting parameters by city, category, rooms, price to create smaller number of requests
        print("Class: Worker; method: execute; portalName=", self.portalName)
        roomsDict = {
            1 : "one",
            2 : "two",
            3 : "three",
            4 : "four",
            5 : "five",
            6 : "six",
            7 : "seven",
            8 : "eight",
            9 : "nine",
            0 : ""
        }
        urlsList = []
        
        if self.portalName == "olx":
            for param in allSearchParameters:
                urlsList.append(
                    {
                        'url' : f"""https://www.olx.pl/d/nieruchomosci/{param.category}/sprzedaz/{param.city}/?search%5Bfilter_enum_rooms%5D%5B0%5D={roomsDict[param.rooms]}&search%5Bfilter_float_price_per_m:to%5D={param.price}""".lower(),
                        'params': {'city':str(param.city), 'category': str(param.category), 'rooms':param.rooms, 'price':param.price},
                        'scrapType': 0  # 0 - list, 1 - detail
                    }
                )
        elif self.portalName=="otodom":
            for param in allSearchParameters:
                urlsList.append(
                    {
                        'url' : f"""/{param.category}/sprzedaz/{param.city}/?search%5Bfilter_enum_rooms%5D%5B0%5D={roomsDict[param.rooms]}&search%5Bfilter_float_price_per_m:to%5D={param.price}""".lower(),
                        'params': {'city':str(param.city), 'category': str(param.category), 'rooms':param.rooms, 'price':param.price},
                        'portal': 'olx',
                        'scrapType': 0 # 0 - list, 1 - detail
                    }
                )
        return urlsList

    @classmethod
    def fromPortalName(cls, portalName: str):
            return cls(portalName)
