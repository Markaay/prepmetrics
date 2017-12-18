from datetime import datetime
from datetime import timedelta
from prepsearchconsole import sc_initsearchconsole, sc_full_export, sc_lp_export
from preploadfile import loadjsonfile

#prepapp
APP_NAME = "frietSeoScience"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"
ABSOLUTE_PATH = "/home/admin/prepmetrics/prepmetrics/production/seoscience/friet/"

#Configuration variables
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SC_URL = "http://www.friet-enzo.nl/"

def seoscienceapp():
    """app to retrieve datasets"""
    #Database connection info
    connectiondata = loadjsonfile(APP_NAME, ABSOLUTE_PATH + "connection_data.json")

    #Database connection info
    clientsecrets = ABSOLUTE_PATH + "client_secrets.json"

    #cache general variables
    currentdate = datetime.now()
    delaydate = (currentdate - timedelta(days=5)).strftime("%Y-%m-%d")

    #Initialize the search console api
    webmasters_service = sc_initsearchconsole(APP_NAME, SCOPES, clientsecrets)

    #get full sc report
    sc_full_export(APP_NAME, webmasters_service, SC_URL, connectiondata, delaydate)

    sc_lp_export(APP_NAME, webmasters_service, SC_URL, connectiondata, delaydate)


def main():
    """initialize the compete app"""
    seoscienceapp()

if __name__ == '__main__':
  main()
