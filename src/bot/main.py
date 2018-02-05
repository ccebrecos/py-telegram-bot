# Libraries
import logging
import telebot
import json

# Relative imports
from res.private.telegram import TOKEN
from res.private.explorer import EXPLORER
from src.rpc.rpc import makeRequest
from src.ws.ws import send, rcv


# Constants
LOGGER = logging.getLogger(__name__)
bot = telebot.TeleBot(TOKEN)

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
    global INIT, SUBS

    chat = message.chat.id

    # Nobody subscribed
    if not INIT:
        INIT = True
        msg = {"type": "new-block"}
        send(msg)
        subscribe(chat)

        LOGGER.debug("Starting loop")
        while INIT:
            result_str = rcv()
            result = json.loads(result_str)

            # Heartbeat
            if result['type'] == "heartbeat":
                LOGGER.debug("Got %s from websocket." % result)

            # New block incoming
            elif result['type'] == "new-block":
                block = result['payload']
                message = "New block at height  " + str(block['height']) + \
                          " with id: " + block['hash'] + ".\n\n"

                message += EXPLORER + "block/" + str(block['height'])
                for chat in SUBS:
                    bot.send_message(chat, message)
        LOGGER.debug("Stopping loop")

    # Loop already running, so just add one chat more to the list
    else:
        subscribe(chat)


@bot.message_handler(commands=['unsub'])
def unsub(message):
    global INIT, SUBS
    chat = message.chat.id

    if chat in SUBS:
        unsubscribe(chat)

        # Nobody subscribed, so let's stop the loop!
        if not SUBS:
            LOGGER.debug("Nobody subscribed ! ")
            INIT = False
            # Unsub from websocket
            msg = {"type": "new-block", "unsubscribe": "true"}
            send(msg)


def subscribe(chat):
    global SUBS

    if chat not in SUBS:
        SUBS.append(chat)
        LOGGER.info("%s subscribed to the push notifications." % chat)
        LOGGER.info("There are %s subscribed." % len(SUBS))

        message = "You are now subscribed to block push notifications !"
        bot.send_message(chat, message)


def unsubscribe(chat):
    global SUBS

    SUBS.remove(chat)
    LOGGER.info("%s subscribed to the push notifications." % chat)
    LOGGER.info("There are %s subscribed." % len(SUBS))

    message = "You are now unsubscribed to block push notifications !"
    bot.send_message(chat, message)


"""
    ADDRESS MONITORING METHODS
"""


@bot.message_handler(commands=['listen'])
def listen(message):
    params = message.text.split()[1:]
    chat, response = message.chat.id, ""

    if not params:
        response = "You must provide the address to listen to"
        bot.send_message(chat, response)
    else:
        addr = params[0]
        if not(len(addr) == 33 or len(addr) == 35):
            response = "The address %s is not valid" % addr
            bot.send_message(chat, response)
        else:
            msg = {"type": "address", "address": addr}
            send(msg)

            LOGGER.debug("%s subscribed to address %s" % (chat, addr))

            response = "Successfully subscribed to address: " + str(addr)
            bot.send_message(chat, response)

            while True:
                result_str = rcv()
                result = json.loads(result_str)

                # Heartbeat
                if result['type'] == "heartbeat":
                    LOGGER.debug("Got %s from websocket." % result)
                # New block incoming
                elif result['type'] == "address":
                    # Get variables
                    addr = result['payload']['address']
                    transaction = result['payload']['transaction']
                    # Info to give
                    message = "New transaction for address " + addr + ".\n" + \
                        "Created transaction "

                    if addr in transaction['inputs'][0]['addresses']:
                        message += "from"
                    elif addr in transaction['outputs'][0]['addresses']:
                        message += "to"

                    txid = transaction['txid']
                    message += " the address with id: " + txid + "\n\n"
                    message += EXPLORER + "tx/" + txid

                    bot.send_message(chat, message)


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
