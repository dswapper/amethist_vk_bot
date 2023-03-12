import sys
from datetime import datetime

from loguru import logger

from bot import bot_

logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.add(f'logs/log_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt', level="DEBUG")

bot_.run_forever()
