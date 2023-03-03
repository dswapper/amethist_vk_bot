import sys
from datetime import datetime

from loguru import logger

from bot.main import bot_

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(f'logs/log_{datetime.now().strftime("%H%M%S_%d%m%Y")}.txt', level="DEBUG")

bot_.run_forever()
