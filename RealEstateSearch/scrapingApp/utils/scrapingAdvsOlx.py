import requests
from bs4 import BeautifulSoup
from django.conf import settings


class ScrapingAdvsOlx():
    """ Scraping all html from url """
    # Download from website all html file and parse it into BeautifulSoup

    def scrapingAdvsOlx(url):
        status = False

        if url == None: 
            url = settings.SCRAPING_URL_DEFAULT
        print("url to scraping", url)

        try:
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            status = True
        except:
            doc = ""
            

        return { 'data': doc, 'status': status}


class CreateUrl():
    """ Create url from list of dict with parameters """
    
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

    def createUrlsOlx(self, params):
        
        urlsList = []
        for param in params:
            urlsList.append(
                {
                    'url' : f"""https://www.olx.pl/d/nieruchomosci/{param['category']}/sprzedaz/{param['city']}/?search%5Bfilter_enum_rooms%5D%5B0%5D={self.roomsDict[param['rooms']]}&search%5Bfilter_float_price_per_m:to%5D={param['price']}""".lower(),
                    'param': param
                }
            )

        return urlsList


class GetFromApiAttrsForUrl():
    """ GET from API attributes create search url. """

    def getFromApiAttrsForUrl():
        """ GET request to api """
        
        print('getFromRestApi: Start')

        dbFromApi = ""
        status = False
        try:
            response = requests.get(settings.API_URL)

            if(response.status_code == requests.codes.ok):
                dbFromApi = response.json()
                status = True
        except:
            print("getFromRestApi: Brak połączenia z SearchingSettingsAPI ")

        print('getFromRestApi: Dane wyjściowe:')
        print(dbFromApi)

        return ({'data':dbFromApi, 'status':status})


class CreateSingleQueryParam():
    """ Create list of single query parameters for create url to scraping. """
    # będzie zawsze pracował poprawnie niezależnie od zmian w category lub rooms


    def sortParam(data):
        """ Create list of single query parameters for create url to scraping. """

        print('sortParam: Start')
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

