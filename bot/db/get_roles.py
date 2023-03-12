from bot.db.models import Users
from bot.db.base import db_sync_pool
from sqlalchemy import select

from typing import Dict, List

from loguru import logger
from bot.enums.roles import Roles


# TODO: Refactor (?)
def get_users_with_role() -> Dict[str, List[int]]:  # TODO: Check updates
    artists_sql_query = select(Users.vk_id).where(Users.role == Roles.role_artist)
    admins_sql_query = select(Users.vk_id).where(Users.role == Roles.role_admin)

    with db_sync_pool() as session:
        artists_list = [int(row[0]) for row in session.execute(artists_sql_query)]
        admins_list = [int(row[0]) for row in session.execute(admins_sql_query)]

    logger.info('Getting users with roles')
    return {'admins_list': admins_list, 'artists_list': artists_list}
