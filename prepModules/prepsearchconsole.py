"""All functions for the seoscience tool"""

def sc_initsearchconsole(app, scope, secrets):
    """initialize the search console api"""
    from apiclient.discovery import build
    from oauth2client import tools
    from oauth2client.service_account import ServiceAccountCredentials

    # Set up a Flow object to be used if we need to authenticate.
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        secrets, scopes=scope)

    # Build the service object.
    webmasters_service = build('webmasters', 'v3', credentials=credentials)

    return webmasters_service

def sc_full_export(app, webmasters_service, sc_url, connectiondata, scdate):
    """get complete search console report"""
    from prepdestinations import mysqldestination

    #Add complete set of data to *sc_full table
    add_full = ("INSERT INTO " + connectiondata["con_full_table"] + " "
	             "(sc_date, query, landing_page, device, country, impressions, clicks, ctr, position)"
	             "VALUES (%(sc_date)s, %(query)s, %(landing_page)s, %(device)s, %(country)s, %(impressions)s, %(clicks)s, %(ctr)s, %(position)s)")

    #data for request
    query_data_request = {
        'startDate': scdate,
        'endDate': scdate,
        'dimensions': ['query', 'page', 'device', 'country'],
        #'rowLimit': 5000
    }
    #execute query to api
    query_data_response = webmasters_service.searchanalytics().query(
        siteUrl=sc_url, body=query_data_request).execute()
    print(query_data_response)

    #sent data to destination
    for row in query_data_response["rows"]:
        sc_full = {
            "sc_date": scdate,
            "query": row["keys"][0],
            "landing_page": row["keys"][1],
            "device": row["keys"][2],
            "country": row["keys"][3],
            "impressions": row["impressions"],
            "clicks": row["clicks"],
            "ctr": row["ctr"],
            "position": row["position"]
        }
        print(sc_full)  
        #push to database
        mysqldestination(app, connectiondata, add_full, sc_full)

def sc_lp_export(app, webmasters_service, sc_url, connectiondata, scdate):
    """get complete search console report"""
    from prepdestinations import mysqldestination

    #Add complete set of data to *sc_full table
    add_lp = ("INSERT INTO " + connectiondata["con_full_lp"] + " "
	             "(sc_date, query, landing_page, device, country, impressions, clicks, ctr, position)"
	             "VALUES (%(sc_date)s, %(query)s, %(landing_page)s, %(device)s, %(country)s, %(impressions)s, %(clicks)s, %(ctr)s, %(position)s)")

    #data for request
    query_data_request = {
        'startDate': scdate,
        'endDate': scdate,
        'dimensions': ['page', 'device', 'country'],
        #'rowLimit': 5000
    }
    #execute query to api
    query_data_response = webmasters_service.searchanalytics().query(
        siteUrl=sc_url, body=query_data_request).execute()
    print(query_data_response)

    #sent data to destination
    for row in query_data_response["rows"]:
        sc_lp = {
            "sc_date": scdate,
            "landing_page": row["keys"][0],
            "device": row["keys"][1],
            "country": row["keys"][2],
            "impressions": row["impressions"],
            "clicks": row["clicks"],
            "ctr": row["ctr"],
            "position": row["position"]
        }
        print(sc_lp)  
        #push to database
        mysqldestination(app, connectiondata, add_lp, sc_lp)
