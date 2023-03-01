from vkbottle import Bot
from bot.config import Config
from bot.handlers import labelers
from bot.middleware import middlewares

bot_ = Bot(
    token=Config.VK_TOKEN
)

for labeler in labelers:
    bot_.labeler.load(labeler)

for middleware in middlewares:
    bot_.labeler.message_view.register_middleware(middleware)
