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

    def sortParam(data):
        """ Create list of single query parameters for create url to scraping. """
        #allSearchParameters = SearchingSettings.objects.filter(category__categoryName ==)

        queryParam = []
        cities = set([x['city'] for x in data])
        
        print('sortParam: city=', cities)

        category = {}
        for city in cities:
            category = set([x['category'] for x in data if x['city'] == city])
        
            print('sortParam: category=', category)

            for cat in category:
                rooms = set([x['rooms'] for x in data if x['category'] == cat and x['city'] == city])
                
                print('sortParam: rooms=', rooms)
                
                price = []
                for room in rooms:
                    price = [x['price'] for x in data if x['category'] == cat and x['rooms'] == room and x['city'] == city] 

                    print('sortParam: price=', max(price))

                    queryParam.append({'city':city, 'category': cat, 'rooms':room, 'price':max(price)})

        print('sortParam: Dane wyjściowe:')
        print(queryParam)

        return queryParam


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
