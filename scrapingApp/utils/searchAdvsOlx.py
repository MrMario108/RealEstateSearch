from bs4 import BeautifulSoup
import requests
import re
from scrapingAdvsOlx import ScrapingAdvsOlx


class SearchAdvsOlx(ScrapingAdvsOlx):

    def __init__(self):
        self.tableOfAds = ""
        super().__init__()

    
    def findTable(self, doc):
        """ Return parent div with all finded advertisements """
        
        print("findTable: Start")
        
        returnedTable = ""
        
        # zabezpieczenie przed zerową ilością nieruchomości
        try:
            zeroTest = doc.body.find("div", {"data-testid": "total-count"})
            #print("findTable: zeroTest ==",zeroTest)
            zeroTest = zeroTest.find(text=re.compile(""))
            #print("findTable: zeroTest 1=",zeroTest)
            patern = re.compile(r"\d+")
            zeroTest = patern.search(str(zeroTest))
            #print("findTable: zeroTest 2=",zeroTest.group())
        
            zeroTest = int(zeroTest.group())
            status = True

        except:
            zeroTest = 0
            status = False

        if zeroTest > 0:
            self.tablesOfAds = doc.body.div.contents
            self.tablesOfAds = doc.find_all("div", class_="css-pband8")
            
            for table in self.tablesOfAds:
                if "Sprawdź ogłoszenia w większej odległości:" not in str(table.previous_sibling):
                    returnedTable +=str(table)

        print("findTable: Returned data - len=")
        print(len(returnedTable))

        return {'data': returnedTable, 'status': status}


    def findAdv(self, table):
        """ Create list of advertisements from a given html div """

        print('findAdv: Start')

        table = BeautifulSoup(table, "html.parser")
        listOfAdvs = table.find_all(attrs={"data-cy":"l-card"})

        print('findAdv: Returned date - len=',len(listOfAdvs))
        return listOfAdvs



    # zabezpieczenie przed zerową ilością nieruchomości
    #zeroTest = BeautifulSoup("""<div data-testid="total-count">Znaleźliśmy  12 ogłoszeń</div>""", "html.parser")
    #print("findTable: zeroTest ==",zeroTest)
    #
    #zeroTest = zeroTest.find(text=re.compile(""))
    #print("findTable: zeroTest 1=",zeroTest)
    #
    #patern = re.compile(r"\d+")
    #zeroTest = patern.search(str(zeroTest))
    #print("findTable: zeroTest 2=",zeroTest.group())