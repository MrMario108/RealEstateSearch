import requests
from olxSearch.models import SearchingSettings
from .scraper import Scraper

class Worker():
    def __init__(self):
        pass
        #self.name = name
        #self.url = url
        #self.scraper = scraper
        #self.database = database
    
    @classmethod
    def createRequestsOlx(self, allSearchParameters):
        # create requests from search parameters
        # for toDo: sorting parameters by city, category, rooms, price to create smaller number of requests
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
        for param in allSearchParameters:
            urlsList.append(
                {
                    'url' : f"""https://www.olx.pl/d/nieruchomosci/{param.category}/sprzedaz/{param.city}/?search%5Bfilter_enum_rooms%5D%5B0%5D={roomsDict[param.rooms]}&search%5Bfilter_float_price_per_m:to%5D={param.price}""".lower(),
                    'params': {'city':str(param.city), 'category': str(param.category), 'rooms':param.rooms, 'price':param.price}
                }
            )
        return urlsList

    @classmethod
    def getSearchParameters(self):
        # get search parameters from model database
        allSearchParameters = SearchingSettings.objects.all()
        if allSearchParameters.count != 0:
            #print(allSearchParameters[0].)
            return allSearchParameters
        else:
            raise ValueError("No search parameters in database")

    @classmethod
    def from_name(self, name: str, allsearchParameters):
        if name == "olx.pl-list":
            requests = self.createRequestsOlx(allsearchParameters)
            return name, requests

        elif name == "otodom.pl":
            return name, requests
        else:
            raise ValueError("Worker name is not valid")


#@app.task
class TestScrap():
    def worker(worker_name: str):
        # you can use worker_name to use different kinds of workers to get requests/urls
        allsearchParameters = Worker.getSearchParameters()
        if allsearchParameters != None:
            name, requests = Worker.from_name(worker_name, allsearchParameters)
            print("Class: TestScrap; method: worker; List of url =",requests)
            for request in requests:
                downloader(request, name)
                #downloader.delay(requests)
        else:    
            raise ValueError("Class: TestScrap; method: worker; messege: No search parameters in database")



#@app.task
def downloader(request, name):
    # Download html file and run scraper

    # for test - for prod leaf only else body
    htmlBody = None
    if name == "olx.pl-list":
        with open('olx-list.html', 'r') as f:
            htmlBody = f.read()
    elif name == "olx.pl-details":
        with open('olx-detail.html', 'r') as f:
            htmlBody = f.read()
    
    print('Class: ; method: downloader; Returned date: msg = , name= ',name, file=open("log.txt", "a"))
    
    if htmlBody:
        scraper(htmlBody, name, request['params'])
    else:
        session = requests.Session()
        response = session.get(request['url'], timeout=5)
        if response.status_code == 200:
            scraper(response.text, name, request['params'])
            #scraper.delay(response)


#@app.task
def scraper(response, name, params):
    # Run scraper and save data to database
    
    print('Class: ; method: scraper; Returned date: msg = Start scraper, name= ',name, file=open("log.txt", "a"))
    scraps, name, requests = Scraper.execute(response, name, params)
    print('Class: ; method: scraper; Returned date: msg = Done scrap, name= ',name, file=open("log.txt", "a"))
    
    if name=="saveToDb": #len(scraps) != 0:
        print('Class: ; method: scraper; Returned date: msg = Start save detail to database, name, len urls= ', file=open("log.txt", "a"))
        
        #for scrap in scraps:
        print('Class: ; method: scraper; Returned date: msg = Try to save detail to database; scrap =',scraps, file=open("log.txt", "a"))

            #Database().merge(scrap)
    if name=="olx.pl-details": #len(requests) != 0:
        print('Class: ; method: scraper; Returned date: msg = Start scraper detail, name, len urls= ',name, len(requests), file=open("log.txt", "a"))
        
        for request in requests:
            print('Class: ; method: scraper; Returned date: msg = Start scraper detail for url, url, params= ',request["url"], request["params"], file=open("log.txt", "a"))
            downloader(request, name)
            #downloader.delay(request)



if __name__ == '__main__':
    pass