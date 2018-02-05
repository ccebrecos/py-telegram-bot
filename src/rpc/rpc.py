# Libraries
import json
import logging
import requests

# Relative imports
from res.private.rpc import AUTH
from res.private.rpc import URL

# Constants
LOGGER = logging.getLogger(__name__)
PAYLOAD = {
        "method": "",
        "params": [],
        "id": 1,
}


# Functions
def makeRequest(payload, head={}):
    LOGGER.debug("Making request with %s" % payload)
    response = requests.post(URL, data=json.dumps(payload), headers=head,
                             auth=AUTH).json()
    LOGGER.debug("Respones is: %s" % response['result'])
    return response['result']
