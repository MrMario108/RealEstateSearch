import requests
import json

from django.conf import settings
# , flush=True command for printing statmants to web consol and log file
# direct log file
# https://www.pythonanywhere.com/user/aotdemouser/files/var/log/alwayson-log-837.log
# console command to see online logs 
# tail -f /var/log/alwayson-log-837.log


class SaveAdvDetailsOlx():
    """ Create record in db """
    def __init__(self):
        self.dbFromApi = self.getFromRestApi()
    

    def saveToFile(data, path="", filename='savedAdv.txt'):
        
        with open((path+filename), "a", encoding="utf-8") as file:
            for adv in data:
                file.write(str(adv) + "\n")
        print("Saved in file", flush=True)

    def checkIsInDb(self, advToCheck):
        """ check if data is in database. if id is 0 it means that script does not find it. In this case it compare (price, rooms, link), but it is possible to have duplicates."""

        if int(advToCheck.get('advId')) != 0 :
            for adv in self.dbFromApi:
                #print(adv)

                if int(adv.get('advId')) == int(advToCheck.get('advId')):
                    print('jest w bazie:')
                    return True
                    break
        else :
            for adv in self.dbFromApi:
                #print(adv)

                if int(adv.get('price')) == int(advToCheck.get('price')) and int(adv.get('rooms')) == int(advToCheck.get('rooms')) and str(adv.get('link')) == str(advToCheck.get('link')):
                    print('jest w bazie:')
                    return True
                    break
    
        return False

    def getFromRestApi(self):
        """ GET request to api """
        response = requests.get(settings.API_OLXSEARCH_URL)
        
        if(response.status_code != requests.codes.ok):
            print('Error connect database', flush=True)
        else:
            pass
        dbFromApi = response.json()

        # print(dbFromApi, flush=True)

        return dbFromApi


    @classmethod
    def postToRestApi(self, data):
        """ POST request to api to create a new found advertisements """
        
        print('postToRestApi: Start')

        #data = [{
        #    'advId': 111111111,
        #    'link': '1',
        #    'pic': '1',
        #    'title': 'Test Rest Api',
        #    'price': 1.0,
        #    'date_published': '10 listopada 2022',
        #    'rooms': 1,
        #    'area': 1.0,
        #    'category': 'mieszkania',
        #    'city': 'ruda-slaska',
        #}]

        posted = 0
        for adv in data:
            print("Check and trying to save: ", flush=True)
            print(adv)
            if self.checkIsInDb(adv) != True:
                try:
                    response = requests.post(settings.API_OLXSEARCH_URL, json = adv)
                    
                    if(response.status_code != requests.codes.created):
                        print('postToRestApi: Error - not created in database', flush=True)
                    else:
                        posted += 1
                        print('postToRestApi: Posted', flush=True)

                        print("postToRestApi: Saved in database", flush=True)
                    
                    print("postToRestApi: Code: ", response.status_code, flush=True)

                except:
                    print("postToRestApi: Unknown error - not created database", flush=True)
            else:
                print('postToRestApi: Already in database', flush=True)
        
        print("postToRestApi: posted", posted, 'advaresments')
            
# API pythonanywher
# --------------------------------
# import requests
# username = 'RealEstateSearch'
# token = '38c81ae3f829ccdcefbcba6e335d06af3a3f58c6'
# 
# response = requests.get(
#     'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
#         username=username
#     ),
#     headers={'Authorization': 'Token {token}'.format(token=token)}
# )
# if response.status_code == 200:
#     print('CPU quota info:')
#     print(response.content)
# else:
#     print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
