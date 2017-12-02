"""jumbo facebook owned public data app.
end of discription.
"""
#dependencies
import sys
sys.path.append('../../../prepModules')
from prepfacebookowned import fb_httpbuilderpublic, fb_ownedpubliccomplete
from prephttp import httpjson
from preploadfile import loadjsonfile

#prepapp
APP_NAME = "jumboSocialOwned"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"

def fbownedpublicapp():
    """python function that exports all public owned data.
    end of discription.
    """

    #Open access_data.json file
    accessdata = loadjsonfile(APP_NAME, "access_data.json")
    #Database connection info
    connectiondata = loadjsonfile(APP_NAME, "connection_data.json")

    #cache general variables
    contextdata = {
        "current_date_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_date": datetime.now(),
        "last_week_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
        "yesterday_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
    #pages to scrape
    pages_to_scrape = ["jumbosupermarkten", "PLUSsupermarkt", "EMTESUPERMARKTEN", "Dirksupermarkten", "CoopSupermarkten", "lidlnederland", "JanLindersSupermarkten", "DEENSupermarkten", "albertheijn"]
    page_loop = 0

    #loop through pages in array
    for page in pages_to_scrape:
        #construct request for page data
        constructedrequest = fb_httpbuilderpublic(APP_NAME, pages_to_scrape[page_loop], 16, 1500, 6000, accessdata["fb_access_token"])
        print(constructedrequest)

        #retrieve page data json from api
        requestjson = httpjson(APP_NAME, constructedrequest, 30, connectiondata)

        #procus complete public facebook data tables
        fb_ownedpubliccomplete(APP_NAME, requestjson, contextdata, connectiondata, 10)

        #increment top page loop
        page_loop = page_loop+1

if __name__ == '__main__':
    fbownedpublicapp()
