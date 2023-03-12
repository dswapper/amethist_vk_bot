from vkbottle import Bot, API
from bot.config import Config
from bot.handlers import labelers, state_dispenser
from bot.middleware import middlewares


bot_ = Bot(
    token=Config.VK_TOKEN,
    state_dispenser=state_dispenser
)

for labeler in labelers:
    bot_.labeler.load(labeler)

for middleware in middlewares:
    bot_.labeler.message_view.register_middleware(middleware)
