from bs4 import BeautifulSoup
from .searchAdvsOlx import SearchAdvsOlx
from .searcherAdvDetailsOlx import SearcherAdvDetailsOlx
from .saveAdvDetailsOlx import SaveAdvDetailsOlx
from datetime import datetime

class Scraper():
    def __init__(self, portalName, scrapType) -> None:
        self.portalName = portalName
        self.scrapType = scrapType

    @classmethod
    def fromPortalName(cls, portalName, scrapType):
        return cls( portalName, scrapType)

    def execute(self, requests, params):
        scrapedDetail  = ""
        response = []
        print('\nClass: Scraper; method: execute; Starting; Returned date: requests len =',len(requests),"\n",file=open("log.txt", "a"))

        if self.portalName == "olx" and self.scrapType == 0:
            self.portalName, responseList = ScrapOlx.scrapLinks(requests)
            for responseTemp in responseList:
                updatedParams = params.copy()
                updatedParams["url"] = responseTemp
                response.append(
                    {
                        "params" : updatedParams,
                        "url": responseTemp
                    }
                )
            self.scrapType = 1
        elif self.portalName == "olx" and self.scrapType == 1:
            scrapedDetail = ScrapOlx.scrapDetails(requests, params)
        elif self.portalName == "otodom" and self.scrapType == 0:
            scrapedDetail = "" # ScrapOtodom.scrapDetails(response, params)
        else:
            raise ValueError(f"Class:Scraper; method: execute; Message: Scraper name is not valid. Name= {self.portalName}")
        
        return scrapedDetail, self.portalName, response

class ScrapOlx():
    @classmethod
    def scrapDetails(self, response, params):
        """Method with sets of complex methods to scrape all data from sell advertisement"""
        """not all advs have all params also her are some params that are not in database model
        for add to database model in the future"""

        print('Class: ScrapOlx; method: scrapDetails; msg= Start scrap detail; ', file=open("log.txt", "a"))

        soup = BeautifulSoup(response, "html.parser")
        
        categories = soup.body.find_all("li", {"data-testid":"breadcrumb-item"})
        categories = [i.find("a").text for i in categories]

        print('ScrapLoger: \n', file=open("scrapLoger.txt", "a"))
        print('\nScrapLoger: Scraped categories=', categories, file=open("scrapLoger.txt", "a"))

        # check again if category is real estate
        if "Nieruchomości" not in categories:
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not real estate; categories: ",categories, file=open("log.txt", "a"))
            return False
                
        # check again if category is correct with params what we looking for
        if params['category'] not in categories:  # for example "Mieszkania"
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not what we looking for; categories: ",categories, ";looking for: ", params['category'], file=open("log.txt", "a"))
            return False

        # check again if category is salles
        if "Sprzedaż" not in categories:  # for example "Mieszkania"
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not what we looking for; categories: ",categories, ";looking for: Sprzedaż", file=open("log.txt", "a"))            
            return False

        # check again if city is what we looking for
        cityBool = False
        for city in categories:
            city = city.split(" ")
            if params['city'] in city:  # for example "Warszawa"
                cityBool = True
                break
        if cityBool == False:
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = City is not what we looking for; categories: ",categories, ";looking for: ", params["city"], file=open("log.txt", "a"))
            return False
        
        pic = soup.body.find(class_="swiper-zoom-container")
        pic = pic.find("img")["src"]

        print('\nScrapLoger: Scraped url pic=', pic, file=open("scrapLoger.txt", "a"))
        
        dataPosted = soup.body.find("span",{"data-cy":"ad-posted-at"}).string
        dataPosted = self.formatDate(dataPosted)
        
        print('\nScrapLoger: Scraped dataPosted=', dataPosted, file=open("scrapLoger.txt", "a"))

        title = soup.body.find("h1",{"data-cy":"ad_title"}).string
        print('\nScrapLoger: Scraped title=', title, file=open("scrapLoger.txt", "a"))

        price = soup.body.find("div",{"data-testid":"ad-price-container"}).find("h3").strings
        price = [i for i in price]
        price = int(price[0].strip().replace(' ',''))
        print('\nScrapLoger: Scraped price=', price, file=open("scrapLoger.txt", "a"))

        paramsGroup = soup.body.find_all("li",{"class":"css-1r0si1e"})
        paramsGroup = [i.find("p").text for i in paramsGroup]
        # paramsGroup has variable len 
        print('\nScrapLoger: Scraped paramsGroup=', paramsGroup, file=open("scrapLoger.txt", "a"))
        for param in paramsGroup:
            catParam = param.split()
            #print('ScrapLoger: Scraped catParam[0]=', catParam[0],"; ", file=open("scrapLoger.txt", "a"))
            if catParam[0] == "Prywatne" or catParam[0] == "Prywatne":
                ownerCategory = paramsGroup[0]
            if catParam[0] == "Poziom:":
                level = catParam[1]
            if catParam[0] == "Rynek:":
                market = catParam[1]
            if catParam[0] == "Rodzaj":
                buildingType = catParam[2]
            if catParam[0] == "Powierzchnia:":
                area = catParam[1]
                area = float(area.replace(',','.'))
            if catParam[0] == "Liczba":
                rooms = catParam[2]
            
        priceSquer = round(price//area)
        description = soup.body.find("div",{"data-cy":"ad-description"})
        id = soup.body.find("div",{"data-cy":"ad-footer-bar-section"}).find("span").strings
        id = [i for i in id if len(i) > 4]
        # ['Prywatne', 'Cena za m²: 76.74 zł/m²', 'Poziom: 9', 'Umeblowane: Tak', 'Rynek: Pierwotny', 'Rodzaj zabudowy: Apartamentowiec', 'Powierzchnia: 43 m²', 'Liczba pokoi: 2 pokoje']
        scraps={
            "advId":    id[0],
            "link":     params['url'],
            "pic":      pic,
            "title":    title,
            "price":    price,
            "date_published": dataPosted,
            "area":     area,
            "category": params['category'],
            "rooms":    rooms,
            "city":     params['city'],
        }
        print('ScrapLoger: Finish values=', scraps,"; ", file=open("scrapLoger.txt", "a"))

        return scraps

    @classmethod
    def changeMonth(self, month):
        match month:
            case "styczeń":
                return "01"
            case "luty":
                return "02"
            case "marzec":
                return "03"
            case "kwiecień":
                return "04"
            case "maj":
                return "05"
            case "czerwiec":
                return "06"
            case "lipiec":
                return "07"
            case "sierpień":
                return "08"
            case "wrzesień":
                return "09"
            case "październik":
                return "10"
            case "listopad":
                return "11"
            case "grudzień":
                return "12"
            case _:
                return "01"
    
    @classmethod
    def formatDate(self, date):
        """Input data: "1 stycznia 2023" Output data: datatime: 01-01-2023"""

        date = date.split(" " or "-")
        date[1] = self.changeMonth(date[1].lower())
        try:
            date = datetime.strptime(date[0]+"-"+date[1]+"-"+date[2], "%d-%m-%Y")
        except:
            date = datetime.now()
        return date

    @classmethod
    def scrapLinks(self,response):

        
        soup = BeautifulSoup(response, "html.parser")
        print('Class: ScrapOlx; method: scrapLinks; Returned date: soup-len =',len(soup),"Type= ",type(soup), file=open("log.txt", "a"))
        with open('soup.txt', 'w') as f:
            f.write(str(soup))

        grid = soup.body.find("div", {"data-testid":"listing-grid"})
        print('Class: ScrapOlx; method: scrapLinks; Returned date: grid-len =',len(grid),file=open("log.txt", "a"))
        with open('grid.txt', 'w') as f:
            f.write(str(grid))
        cards = grid.find_all(attrs={"data-cy":"l-card"})
        print('Class: ScrapOlx; method: scrapLinks; Returned date: cards-len =',len(cards),file=open("log.txt", "a"))
        with open('cards.txt', 'w') as f:
            f.write(str(cards))

        links = []
        for card in cards:
            link = card.a["href"]

            if not 'https://www.otodom.pl/pl/oferta' in link:

                if not "/d/oferta" in link:

                    if not "/d/nieruchomosci" in link:
                        print('Class: ScrapOlx; method: scrapLinks; Returned date: msg = url error, url=', link, file=open("log.txt", "a"))

                        return False
            else:
                portalName = "otodom"

            if not "https" in link:
                link = "https://www.olx.pl"+link
                portalName = "olx"
            
            links.append(link)
        
        with open('links.txt', 'w') as f:
            for link in links:
                f.write(link+'\n')
        return portalName, links
    


#childGenerator() -> children
#nextGenerator() -> next_elements
#nextSiblingGenerator() -> next_siblings
#previousGenerator() -> previous_elements
#previousSiblingGenerator() -> previous_siblings
#recursiveChildGenerator() -> descendants
#parentGenerator() -> parents

#parse_only = SoupStrainer('item')
#soup = BeautifulSoup(data, "html.parser", parse_only=parse_only)
#for item in soup.children:
#    print(item.get_text())