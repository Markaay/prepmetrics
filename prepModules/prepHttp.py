"""functions that retrieve info from http sources"""
#Get JSON w
def httpjson(app, http, timeoutseconds):
    """function that handles all json request in python"""
    import urllib2
    import json

    #the complete unescaped url to crawl
    request_uri = urllib2.Request(http)
    try:
        api_response = urllib2.urlopen(request_uri, timeout=timeoutseconds)
        response_string = api_response.read().decode('utf-8')
        json_data = json.loads(response_string)
        return json_data
    except urllib2.HTTPError, err:
        if err.code == 404:
            return 'Page not found!'
        elif err.code == 403:
            return 'Access denied!'
        elif err.code == 500:
            return 'Timeout error!'
        else:
            return 'Other HTTP error!'
    except urllib2.URLError, err:
        return 'Other URL error!'
