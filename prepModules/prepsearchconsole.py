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

def sc_full_export(app, sc_url, searchconsole, querydate, searchtype, startrow):
    """get complete search console report"""

    #data for request
    query_data_request = {
        'startDate': querydate,
        'endDate': querydate,
        'dimensions': ['date', 'query', 'page', 'device', 'country'],
        'rowLimit': 5000,
        'startRow': startrow,
        'searchType': searchtype
    }
    #execute query to api
    query_data_response = searchconsole.searchanalytics().query(
        siteUrl=sc_url, body=query_data_request).execute()
    print(query_data_response)

    #sent data to destination
    return query_data_response

def sc_lp_export(app, sc_url, searchconsole, querydate, searchtype, startrow):
    """get complete search console report"""
    query_data_request = {
        'startDate': querydate,
        'endDate': querydate,
        'dimensions': ['date', 'page', 'device', 'country'],
        'rowLimit': 5000,
        'startRow': startrow,
        'searchType': searchtype
    }

    query_data_response = searchconsole.searchanalytics().query(
        siteUrl=sc_url, body=query_data_request).execute()
    
    #sent data to destination
    return query_data_response

def sc_query_export(app, sc_url, searchconsole, querydate, searchtype, startrow):
    """get complete search console report"""
    query_data_request = {
        'startDate': querydate,
        'endDate': querydate,
        'dimensions': ['date', 'query', 'device', 'country'],
        'rowLimit': 5000,
        'startRow': startrow,
        'searchType': searchtype
    }

    query_data_response = searchconsole.searchanalytics().query(
        siteUrl=sc_url, body=query_data_request).execute()
    
    #sent data to destination
    return query_data_response
