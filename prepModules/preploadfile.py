"""top docstring.
end of discription.
"""

import json
from prepModules.preplogger import applogger

def loadjsonfile(app, jsonpath):
    """function that reads the json path and returns it to the app"""
    logger = applogger(app)
    #Open access_data.json file
    with open(jsonpath, 'r') as filedata:
        jsondata = json.load(filedata)
        logger.debug('json file read')
    return jsondata
