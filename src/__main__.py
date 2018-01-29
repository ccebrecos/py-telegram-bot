# Absolute imports
import logging
import telebot

# Relative imports
import src.log
from src.cli.arguments.constants import LOGS_LEVELS, LOGS
from res.private.telegram import TOKEN
from src.rpc.rpc import makeRequest

# Constants
LOGGER = logging.getLogger(__name__)
bot = telebot.TeleBot(TOKEN)


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


@bot.message_handler(func=lambda m: True)
def command(message):
    LOGGER.debug("message %s, received from: %s", message.text,
                 message.from_user.username)
    meth = message.text.split()[0]
    params = message.text.split()[1:]
    p = {"method": meth, "params": params, "id": 1}

    if meth == "dumpprivkey":
        result = "Claro que si guapi"
    elif meth == "stop":
        result = "mmm nope"
    else:
        LOGGER.debug("making request with %s", p)
        result = makeRequest(p)
        result = str(result)

    if result == "None":
        result = "There's no response for that request."
    LOGGER.debug("response: %s", result)
    bot.reply_to(message, result)


if __name__ == "__main__":

    # Switching log level
    root_logger = logging.getLogger()
    root_logger.setLevel(LOGS_LEVELS[LOGS.index('debug')])
    # Welcome
    LOGGER.info("Welcome!")
    LOGGER.debug("token: %s", TOKEN)
    bot.polling()
    # Exiting
    LOGGER.info("Bye!")
