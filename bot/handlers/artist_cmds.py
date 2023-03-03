from vkbottle.bot import BotLabeler, Message, rules

from bot.db.init_roles import artists_ids, admins_ids

artist_labeler = BotLabeler()
artist_labeler.auto_rules = [rules.FromPeerRule(artists_ids + admins_ids)]  # TODO: при добавлении обновлять список


