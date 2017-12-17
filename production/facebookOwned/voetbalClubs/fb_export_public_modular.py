"""voetbalclubs facebook owned public data app"""
#dependencies
import json
from prepfacebookowned import fb_httpbuilderpublic, fb_ownedpubliccomplete
from prephttp import httpjson

#prepapp
APP_NAME = "voetbalSocialOwned"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"

def fbownedpublicapp():
    """python function that exports all public owned data"""

    #Open local json files
    def loadjsonfile(jsonpath):
        """function that reads the json path and returns it to the app"""
        #Open access_data.json file
        with open(jsonpath, 'r') as filedata:
            jsondata = json.load(filedata)
        return jsondata

    #Open access_data.json file
    accessdata = loadjsonfile("access_data.json")
    #Database connection info
    connectiondata = loadjsonfile("connection_data.json")

    #pages to scrape
    pages_to_scrape = ["afcajax", "PSV", "feyenoord",
                       "AZAlkmaar", "FCUtrecht1970", "ADODenHaag",
                       "peczwolle", "VitesseArnhem", "scheerenveen",
                       "HeraclesAlmelo", "VVV.Venlo", "FCGroningen",
                       "excelsiorrdam", "WillemIITilburg", "FCTwente",
                       "NACnl", "SpartaRotterdam", "RodaJCKerkrade",
                       "NECNijmegen"]
    page_loop = 0

    #loop through pages in array
    for page in pages_to_scrape:
        #construct request for page data
        constructedrequest = fb_httpbuilderpublic(APP_NAME, pages_to_scrape[page_loop],
                                                  25, 1500, 6000, accessdata["app_access_token"])
        print(constructedrequest)
        #retrieve page data json from api
        requestjson = httpjson(APP_NAME, constructedrequest, 40)
        print(requestjson)

        #procus complete public facebook data tables
        fb_ownedpubliccomplete(APP_NAME, requestjson, connectiondata, 10)

        #increment top page loop
        page_loop = page_loop+1

if __name__ == '__main__':
    fbownedpublicapp()
