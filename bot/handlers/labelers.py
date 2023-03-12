from vkbottle.bot import BotLabeler, rules
from vkbottle.dispatch.rules.base import ABCRule
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from bot.db.get_roles import get_users_with_role

artist_labeler = BotLabeler()
admin_labeler = BotLabeler()
order_labeler = BotLabeler()


def get_admin_role_autorule(labeler: BotLabeler) -> List[ABCRule]:
    new_rule = rules.FromPeerRule(get_users_with_role()['admins_list'])
    if len(labeler.auto_rules) > 1:
        for n, rule in enumerate(labeler.auto_rules):
            if isinstance(rule, rules.FromPeerRule):
                labeler.auto_rules[n] = new_rule
    else:
        labeler.auto_rules = [new_rule]
    return labeler.auto_rules


def get_artist_role_autorule(labeler: BotLabeler) -> List[ABCRule]:
    new_rule = rules.FromPeerRule(get_users_with_role()['admins_list'] + get_users_with_role()['artists_list'])
    if len(labeler.auto_rules) > 1:
        for n, rule in enumerate(labeler.auto_rules):
            if isinstance(rule, rules.FromPeerRule):
                labeler.auto_rules[n] = rules.FromPeerRule(get_users_with_role()['admin_list']
                                                           + get_users_with_role()['artist_list'])
    else:
        labeler.auto_rules = [new_rule]
    return labeler.auto_rules
