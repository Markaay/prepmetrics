"""functions that retrieve info from http sources"""
#Get JSON
def httpjson(app, http, timeoutseconds):
    """function that handles all json request in python"""
    import urllib2
    import json
    from preplogger import applogger

    #create logger based on app name
    logger = applogger(app)
    #the complete unescaped url to crawl
    request_uri = urllib2.Request(http)
    try:
        api_response = urllib2.urlopen(request_uri, timeout=timeoutseconds)
        response_string = api_response.read().decode('utf-8')
        json_data = json.loads(response_string)
        logger.debug('data collected: '+ 'json')
        return json_data
    except urllib2.HTTPError, err:
        if err.code == 404:
            logger.error("Page not found!")
            return 'Page not found!'
        elif err.code == 403:
            logger.error('Access denied!')
            return 'Access denied!'
        elif err.code == 500:
            logger.error('Timeout error!')
            return 'Timeout error!'
        else:
            logger.error(err.code)
            return 'Other HTTP error!'
    except urllib2.URLError, err:
        logger.error(err.reason)
        return 'Other URL error!'
