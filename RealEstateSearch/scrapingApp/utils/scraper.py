from bs4 import BeautifulSoup
from .searchAdvsOlx import SearchAdvsOlx
from .searcherAdvDetailsOlx import SearcherAdvDetailsOlx
from .saveAdvDetailsOlx import SaveAdvDetailsOlx
from datetime import datetime

class Scraper():
    def execute(response, name, params):
        scraps  = ""
        requests = []

        if name == "olx.pl-list":
            name, requeststemp = ScrapOlx.scrapLinks(response)
            for request in requeststemp:
                updatedParams = params.copy()
                updatedParams["url"] = request
                requests.append(
                    {
                        "params" : updatedParams,
                        "url": request
                    }
                )
            print('Class: Scraper; method: execute; Returned date: requests len =',len(requests),file=open("log.txt", "a"))
        elif name == "olx.pl-details":
            scraps = ScrapOlx.scrapDetails(response, params)
            name = "saveToDb"
        elif name == "otodom.pl":
            scraps = "" # ScrapOtodom.scrapDetails(response, params)
            name = "saveToDb"
        else:
            raise ValueError(f"Class:Scraper; method: execute; Message: Scraper name is not valid. Name= {name}")
        
        return scraps, name, requests

class ScrapOlx():
    def __init__(self):
        pass
    @classmethod
    def scrapDetails(self, response, params):
        """Method with sets of complex methods to scrape all data from sell advertisement"""
        """not all advs have all params also her are some params that are not in database model
        for add to database model in the future"""

        print('Class: ScrapOlx; method: scrapDetails; msg= Start scrap detail; ', file=open("log.txt", "a"))

        soup = BeautifulSoup(response, "html.parser")
        
        categories = soup.body.find_all("li", {"data-testid":"breadcrumb-item"})
        categories = [i.find("a").text for i in categories]

        # check again if category is real estate
        if "Nieruchomości" not in categories:
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not real estate; categories: ",categories, file=open("log.txt", "a"))
            return ValueError("Category of this advartesment is not real estate")
        
        # check again if category is correct with params what we looking for
        if params['category'] not in categories:  # for example "Mieszkania"
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not what we looking for; categories: ",categories, ";looking for: ", params['category'], file=open("log.txt", "a"))
            return ValueError("Category of this advartesment is not what we looking for")

        # check again if category is salles
        if "Sprzedaż" not in categories:  # for example "Mieszkania"
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = Category is not what we looking for; categories: ",categories, ";looking for: Sprzedaż", file=open("log.txt", "a"))
            return ValueError("Category of this advartesment is not what we looking for")
        
        # check again if city is what we looking for
        cityBool = False
        for city in categories:
            city = city.split(" ")
            if params['city'] in city:  # for example "Warszawa"
                cityBool = True
                break
        if cityBool == False:
            print("Class: ScrapOlx; method: scrapDetails; Returned date: msg = City is not what we looking for; categories: ",categories, ";looking for: ", params["city"], file=open("log.txt", "a"))
            return ValueError("City of this advartesment is not what we looking for")
        
        pic = soup.body.find(class_="swiper-zoom-container")
        pic = pic.find("img")["src"]
        dataPosted = soup.body.find("span",{"data-cy":"ad-posted-at"}).string
        dataPosted = self.formatDate(dataPosted)
        title = soup.body.find("h1",{"data-cy":"ad_title"}).string
        price = soup.body.find("div",{"data-testid":"ad-price-container"}).find("h3").strings
        price = [i for i in price]
        price = int(price[0].strip().replace(' ',''))
        paramsGroup = soup.body.find_all("li",{"class":"css-1r0si1e"})
        paramsGroup = [i.find("p").text for i in paramsGroup]
        ownerCategory = paramsGroup[0]
        level = paramsGroup[2].split(" ")[1]
        market = paramsGroup[4].split(" ")[1]
        buildingType = paramsGroup[5].split(" ")[2]
        area = paramsGroup[6].split(" ")
        area = float(area[1].strip().replace(',','.'))
        rooms = paramsGroup[7].split(" ")[2]
        priceSquer = round(price//area)
        description = soup.body.find("div",{"data-cy":"ad-description"})
        id = soup.body.find("div",{"data-cy":"ad-footer-bar-section"}).find("span").strings
        id = [i for i in id if len(i) > 4]

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

            if not "https" in link:
                link = "https://www.olx.pl"+link
            links.append(link)
        
        with open('links.txt', 'w') as f:
            for link in links:
                f.write(link)
                f.write('\n')
        name = "olx.pl-details"
        return name, links
    


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