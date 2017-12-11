"""jumbo facebook owned public data app"""
#dependencies
import sys
sys.path.append("../../../prepModules")
from prepfacebookowned import fb_getpageidsmysql, fb_getcommentsentimentmsql
from preploadfile import loadjsonfile

#prepapp
APP_NAME = "jumboSocialOwnedSentiment"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"

def fbownedcommentsentiment():
    """get the sentiment data of yesterday's comments of pages"""
    #Database connection info
    connectiondata = loadjsonfile(APP_NAME, "connection_data.json")
    #sentiment api info
    sentapidata = loadjsonfile(APP_NAME, "sent_api_data.json")

    #get list of ids to loop through
    fb_pages = fb_getpageidsmysql(APP_NAME, connectiondata, 10)

    #get comments for each fb_page of yesterday
    for _ in fb_pages:
        fb_getcommentsentimentmsql(APP_NAME, fb_pages, connectiondata, sentapidata)

if __name__ == '__main__':
    fbownedcommentsentiment()
