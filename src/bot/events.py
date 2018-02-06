# Libraries
import json
import logging
import _thread

# Relative imports
from src.bot.bot import bot
from res.public.explorer import EXPLORER
from src.ws.ws import send, rcv


# Constants
LOGGER = logging.getLogger(__name__)

# GLOBALS
ADDR_SUBS, BLOCK_SUBS, LOOP = {}, [], False


def recv_loop():
    """
    Maintains a loop for listen to received websockets messages. It blocks
    until a message is received and passes it to the propper method to
    handle the response.
    """
    global LOOP

    LOGGER.debug("Starting loop")
    while LOOP:

        result_str = rcv()
        result = json.loads(result_str)

        handle_response(result)

    # Exited loop: nothing to receive
    LOGGER.debug("Stopping loop")


def handle_response(rsp):
    """
    Handles the response from the websocket and treats it in order of the kind
    of the response

    Args:
        rsp (dict): Dictionary with the response received from the websocket
    """
    global BLOCK_SUBS, ADDR_SUBS

    # Heartbeat
    if rsp['type'] == "heartbeat":
        LOGGER.debug("Websocket alive: %s" % rsp)

    # New block incoming
    elif rsp['type'] == "new-block":
        block = rsp['payload']
        message = "New block at height " + str(block['height']) + \
                  " with id: " + block['hash'] + ".\n\n"

        message += EXPLORER + "block/" + str(block['height'])

        # Send messages
        for chat in BLOCK_SUBS:
            bot.send_message(chat, message)

    # New address event incoming
    elif rsp['type'] == "address":
        # Get variables
        addr = rsp['payload']['address']
        transaction = rsp['payload']['transaction']
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

        # Send messages
        for chat in ADDR_SUBS[addr]:
            bot.send_message(chat, message)

    # Unexpected message received
    else:
        LOGGER.debug("Got %s from websocket." % rsp)


def check_stop():
    """
    Checks if there's no need to maintain the loop listening.
    """
    global ADDR_SUBS, BLOCK_SUBS, LOOP

    # Nobody subscribed to anything
    if not BLOCK_SUBS and not ADDR_SUBS:
        LOOP = False


"""
    BLOCKS MONITORING METHODS
"""


def subscribe(chat):
    """
    Adds a chat to the list in order to listen to blocks events.

    Args:
        chat (int): Chat id to subscribe to blocks events
    """
    global BLOCK_SUBS, LOOP
    message = ""

    # First subscriber
    if not BLOCK_SUBS:
        msg = {"type": "new-block"}
        send(msg)

        # Loop not started before
        if not LOOP:
            LOOP = True
            _thread.start_new_thread(recv_loop, ())

    # New subscriber
    if chat not in BLOCK_SUBS:
        BLOCK_SUBS.append(chat)
        LOGGER.info("%s subscribed to the push notifications." % chat)
        LOGGER.info("There are %s subscribed." % len(BLOCK_SUBS))
        message += "You are now subscribed to block push notifications!"

    # Subscriber already subscribed
    else:
        message += "You were already subscribed to block push notifications."

    bot.send_message(chat, message)


def unsubscribe(chat):
    """
    """
    global BLOCK_SUBS
    message = ""

    if chat in BLOCK_SUBS:
        BLOCK_SUBS.remove(chat)
        message += "You're are successfully unsubscribed from block " + \
            "notifications."
        # Unsub from websocket
        if not BLOCK_SUBS:
            msg = {"type": "new-block", "unsubscribe": "true"}
            send(msg)
    else:
        message += "You were not subscribed."

    bot.send_message(chat, message)
    check_stop()


"""
    ADDRESS MONITORING METHODS
"""


def listen(chat, addr):
    """
    Adds a new chat to address transaction events.

    Args:
        chat (int): Chat id to subscribe to address events
        addr (str): Address in order to listen to
    """
    global ADDR_SUBS, LOOP
    message = ""

    # New address to listen to
    if addr not in ADDR_SUBS.keys():
        msg = {"type": "address", "address": addr}
        send(msg)

        result_str = rcv()
        print(result_str)
        result = json.loads(result_str)

        # Check subscription success
        if not result['payload']['success']:
            message += "Failed to subscribe; %s" % result['payload']['message']
        else:
            # Loop not started before
            if not LOOP:
                LOOP = True
                _thread.start_new_thread(recv_loop, ())

            # Add address to list
            ADDR_SUBS[addr] = ADDR_SUBS.get(addr, []) + [chat]

            message += "Successfully subscribed to address %s events" % addr

    bot.send_message(chat, message)


def unlisten(chat, addr):
    """
    """
    global ADDR_SUBS
    message = ""

    if addr not in ADDR_SUBS.keys():
        message = "You were not subscribed to address %s events" % addr
    else:
        ADDR_SUBS[addr].remove(chat)
        message += "Successfully unsubscribed to address %s events" % addr

        if not ADDR_SUBS[addr]:
            del ADDR_SUBS[addr]
            msg = {"type": "address", "address": addr, "unsubscribe": "true"}
            send(msg)

    bot.send_message(chat, message)
    check_stop()
