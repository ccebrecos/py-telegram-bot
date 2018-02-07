# Libraries
import logging

# Relative imports
import src.log
from src.bot.main import bot
from src.cli.arguments.constants import LOGS_LEVELS, LOGS
from src.ws.ws import open_con, close_con


# Constants
LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":

    # Switching log level
    root_logger = logging.getLogger()
    root_logger.setLevel(LOGS_LEVELS[LOGS.index('debug')])
    # Welcome
    LOGGER.info("Welcome!")
    open_con()
    bot.polling()
    # Exiting
    close_con()
    LOGGER.info("Bye!")
