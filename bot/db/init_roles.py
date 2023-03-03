from bot.db.models import Artists, Admins
from bot.db.base import db_sync_pool
from sqlalchemy import select

from loguru import logger

admins_ids = []
artists_ids = []


def init_artists_ids() -> list:
    artists_sql_query = select(Artists.peer_id).where(Artists.is_artist)
    with db_sync_pool() as session:
        result = session.execute(artists_sql_query)
        return [int(row[0]) for row in result]


def init_admins_ids() -> list:
    admins_sql_query = select(Admins.peer_id).where(Admins.is_admin)
    with db_sync_pool() as session:
        result = session.execute(admins_sql_query)
        return [int(row[0]) for row in result]


def init():
    logger.info('Initialising roles')
    global artists_ids, admins_ids
    admins_ids = init_admins_ids()
    artists_ids = init_artists_ids()
    logger.info('Roles initialising complete')


init()
