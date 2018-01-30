# Libraries
import logging

# Relative imports
import src.log
from src.cli.arguments.constants import LOGS_LEVELS, LOGS
from src.bot.main import bot

# Constants
LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":

    # Switching log level
    root_logger = logging.getLogger()
    root_logger.setLevel(LOGS_LEVELS[LOGS.index('debug')])
    # Welcome
    LOGGER.info("Welcome!")
    bot.polling()
    # Exiting
    LOGGER.info("Bye!")
