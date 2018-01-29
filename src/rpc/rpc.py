# Libraries
import json
import requests

# Relative imports
from res.private.rpc import AUTH
from res.private.rpc import URL

# Constants
PAYLOAD = {
        "method": "",
        "params": [],
        "id": 1,
}


# Functions
def makeRequest(payload, head={}):
    response = requests.post(URL, data=json.dumps(payload), headers=head,
                             auth=AUTH).json()
    return response['result']
