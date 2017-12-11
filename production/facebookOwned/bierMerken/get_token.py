"""top docstring.
end of discription.
"""

import sys
sys.path.append('../../../prepModules')
from prepfacebookowned import fb_gettoken

#prepapp information
APP_NAME = "jumboSocialOwned"
PY_VERSION = "2.7"
CREATOR = "prepmetrics"

#token information
STORED_FILE_PATH = "access_data.json"
FB_APP_ID = "189107884825866"
FB_APP_SECRET = "75b2266497016d64a0efdde0dd0d2541"

def fbownedpublictokenrequest():
    """python function that retrieves token to access facebook owned public data.
    end of discription.
    """
    fb_gettoken(APP_NAME, FB_APP_ID, FB_APP_SECRET, STORED_FILE_PATH)
