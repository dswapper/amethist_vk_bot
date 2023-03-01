from vkbottle.bot import BotLabeler, Message, rules

from bot.db.init_roles import artists_ids

artist_labeler = BotLabeler()
artist_labeler.auto_rules = [rules.FromPeerRule(artists_ids)]  # TODO: при добавлении обновлять список

@artist_labeler.message(command='check')
async def check_handler_artist(message: Message):
    await message.answer('Вы художник!')
