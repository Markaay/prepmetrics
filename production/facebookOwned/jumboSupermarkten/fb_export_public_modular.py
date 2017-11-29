"""jumbo facebook owned public data app.
end of discription.
"""
#dependencies
import json
from datetime import datetime
from datetime import timedelta
import sys
sys.path.append('../../../prepModules')
from prepfacebookowned import fb_httpbuilderpublic, fb_ownedpubliccomplete
from prephttp import httpjson

#prepApp
APP_NAME = "jumboSocialOwned"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"

def fbownedpublicapp():
    """python function that exports all public owned data.
    end of discription.
    """

    #Open access_data.json file
    with open('access_data.json', 'r') as accessinformation:
        fb_data = json.load(accessinformation)
    fb_access_token = fb_data["app_access_token"]

    #Database connection info
    connectiondata = {
        "con_ip": "95.85.56.92",
        "con_db": "prepmetrics_db",
        "con_user": "prepper",
        "con_pass": "passa1sdE!fs0!metrics",
        "page_table": "fb_pagedata",
        "post_table": "fb_posts",
        "comment_table": "fb_comments"
    }
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
        constructedrequest = fb_httpbuilderpublic(APP_NAME, pages_to_scrape[page_loop], 16, 1500, 6000, fb_access_token)
        print(constructedrequest)

        #retrieve page data json from api
        requestjson = httpjson(APP_NAME, constructedrequest, 30, connectiondata)

        #procus complete public facebook data tables
        fb_ownedpubliccomplete(APP_NAME, requestjson, contextdata, connectiondata, 10)

        #increment top page loop
        page_loop = page_loop+1

if __name__ == '__main__':
    fbownedpublicapp()
