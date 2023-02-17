from searchAdvsOlx import SearchAdvsOlx
from searcherAdvDetailsOlx import SearcherAdvDetailsOlx, SearchAdvId
from scrapingAdvsOlx import ScrapingAdvsOlx, CreateSingleQueryParam, GetFromApiAttrsForUrl, CreateUrl
from saveAdvDetailsOlx import SaveAdvDetailsOlx
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

from django.conf import settings

if __name__ == '__main__':

    # Connect to api download searching settings and compres to reduce number of urls
    
    
    attrsForUrl = GetFromApiAttrsForUrl.getFromApiAttrsForUrl()

    print("Main: Pobieranie z Api parametrów wyszukiwania", attrsForUrl['status'])
    
    if attrsForUrl['status'] == True:
        queryParamList = CreateSingleQueryParam.sortParam(attrsForUrl['data'])
        urlsListOlx = CreateUrl().createUrlsOlx(queryParamList)
        
        print("Main: Tworzenie url na podstawie danych z API. Ilość zapytań:", len(urlsListOlx))
    else:
        urlsListOlx = []
        urlsListOlx.append(
            {
                'url' : settings.SCRAPING_URL_DEFAULT,
                'param': settings.SCRAPING_URL_PARAM_DEFAULT,
            }
            )
        print("Main: Pobranie default Url z settings", urlsListOlx[0])
    
    # for testing its local file
    #dataWithHtmlSite = scrapingAdvsOlx.findAdvs('index.html')
    if( len(urlsListOlx) > 0):
        
        for url in urlsListOlx:
            print("Main: Rozpoczęcie scraping według poszczególnych url z parametrami")
            dataWithHtmlSite = ScrapingAdvsOlx.scrapingAdvsOlx(url['url'])
            
            if dataWithHtmlSite['status'] == True:
                print("Main: Scraping stronę z listą ogłoszeń:", dataWithHtmlSite['status'])
                searchAdvsOlx = SearchAdvsOlx()
                dataWithHtmlAdvs = searchAdvsOlx.findTable(dataWithHtmlSite['data'])

                if dataWithHtmlAdvs['status'] == True:
                    listOfAdvs = searchAdvsOlx.findAdv(dataWithHtmlAdvs['data'])

                    if(len(listOfAdvs) > 0):
                        print('Main: Zaczynamy skrobać detale o ogłoszeniach')
                        searcherAdvDetailsOlx = SearcherAdvDetailsOlx()

                        table = searcherAdvDetailsOlx.runScrapingAdvDetailsOlx(listOfAdvs, url['param']['rooms'], url['param']['category'], url['param']['city'])

                        if len(table) > 0:
                            print("Main: Rozpoczynamy zapis do db")
                            saveAdvDetailsOlx = SaveAdvDetailsOlx()
                            saveAdvDetailsOlx.postToRestApi(table)
                        else:
                            print('Main: Błąd preszukiwania detali ogłoszeń')

                    else:
                        print('Main: Brak ogłoszeń dla danych parametrów wyszukiwania')
                else:
                    print('Main: Brak ogłoszeń dla danych parametrów wyszukiwania')
            else:
                print('Main: Brak url z parametrami do przeszukania')
