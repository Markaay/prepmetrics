"""top docstring"""

def loadjsonfile(app, jsonpath):
    """function that reads the json path and returns it to the app"""
    import json
    from prepmetrics.prepModules.preplogger import applogger
    logger = applogger(app)
    #Open access_data.json file
    with open(jsonpath, 'r') as filedata:
        jsondata = json.load(filedata)
        logger.debug('json file read')
    return jsondata
