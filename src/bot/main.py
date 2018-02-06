# Libraries
import logging

# Relative imports
from src.bot.bot import bot
from src.bot.events import listen, unlisten
from src.bot.events import subscribe, unsubscribe
from src.rpc.rpc import makeRequest


# Constants
LOGGER = logging.getLogger(__name__)


# GLOBALS
INIT, SUBS = False, []


# Functions
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['help'])
def help(message):
    p = {"method": "help", "params": [], "id": 1}
    LOGGER.debug("making request")
    result = makeRequest(p)
    LOGGER.debug("response: %s", result)
    bot.reply_to(message, result)


"""
    BLOCKS MONITORING METHODS
"""


@bot.message_handler(commands=['sub'])
def sub(message):
    """
    """
    chat = message.chat.id
    subscribe(chat)


@bot.message_handler(commands=['unsub'])
def unsub(message):
    chat = message.chat.id
    unsubscribe(chat)


"""
    ADDRESS MONITORING METHODS
"""


def handle_listener(message, unsubscribe):
    params = message.text.split()[1:]
    chat, response = message.chat.id, ""

    if not params:
        response = "You must provide the address"
        bot.send_message(chat, response)
    else:
        addr = params[0]
        # Subscribe/unsubscribe chat to address events
        if unsubscribe:
            unlisten(chat, addr)
        else:
            listen(chat, addr)


@bot.message_handler(commands=['listen'])
def lst(message):
    handle_listener(message, False)


@bot.message_handler(commands=['unlisten'])
def unlst(message):
    handle_listener(message, True)


@bot.message_handler(func=lambda m: True)
def rpc(message):
    LOGGER.debug("message %s, received from: %s", message.text,
                 message.from_user.username)
    meth = message.text.split()[0]
    params = message.text.split()[1:]
    p = {"method": meth, "params": params, "id": 1}

    if meth == "dumpprivkey":
        result = "This is not the method you're looking for..."
    elif meth == "stop":
        result = "mmm nope"
    else:
        result = makeRequest(p)
        result = str(result)

    if result == "None":
        result = "There's no response for that request."
    LOGGER.debug("response: %s", result)
    bot.reply_to(message, result)
