from vkbottle.bot import BotLabeler, Message, rules

from bot.db.get_roles import get_roles

artist_labeler = BotLabeler()
artist_labeler.auto_rules = [rules.FromPeerRule(get_roles()['artists_list'])]  # TODO: при добавлении обновлять список

