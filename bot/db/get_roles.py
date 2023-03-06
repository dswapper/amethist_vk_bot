from bot.db.models import Users
from bot.db.base import db_sync_pool
from sqlalchemy import select

from loguru import logger
from bot.enums.roles import Roles


def get_roles():
    logger.info('Initialising roles')
    artists_sql_query = select(Users.vk_id).where(Users.role == Roles.role_artist)
    admins_sql_query = select(Users.vk_id).where(Users.role == Roles.role_admin)

    with db_sync_pool() as session:
        artists_list = [int(row[0]) for row in session.execute(artists_sql_query)]
        admins_list = [int(row[0]) for row in session.execute(admins_sql_query)]

    logger.info('Roles initialising complete')
    return {'admins_list': admins_list, 'artists_list': artists_list}