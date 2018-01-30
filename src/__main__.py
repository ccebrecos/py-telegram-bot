# Libraries
import logging

# Relative imports
import src.log
from src.cli.arguments.constants import LOGS_LEVELS, LOGS
from res.private.telegram import TOKEN
from src.bot.main import bot

# Constants
LOGGER = logging.getLogger(__name__)


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
