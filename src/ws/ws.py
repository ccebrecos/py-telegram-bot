# Libraries
import json
import logging
from websocket import create_connection

# Relative imports
from res.private.ws import URL

# Constants
LOGGER = logging.getLogger(__name__)
ws = create_connection(URL)


# Functions
def send(msg):
    """
    Sends a message to the socket endpoint connected to.

    Args:
        msg (dict): data to send through the websocket
    """
    msg = json.dumps(msg, ensure_ascii=False)
    LOGGER.debug("Sending message %s" % msg)
    ws.send(msg)


def rcv():
    """
    Waits until receives a response from the websocket connected to.
    """
    result = ws.recv()
    return result


def close():
    ws.close()
