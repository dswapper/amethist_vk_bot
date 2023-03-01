from bot.db.models import Artists, Admins
from bot.db.base import db_pool
from sqlalchemy import select

import asyncio

admins_ids = []
artists_ids = []


async def init_artists_ids() -> list:
    artists_sql_query = select(Artists.peer_id).where(Artists.is_artist)
    async with db_pool() as session:
        result = await session.execute(artists_sql_query)
        return [int(row[0]) for row in result]


async def init_admins_ids() -> list:
    admins_sql_query = select(Admins.peer_id).where(Admins.is_admin)
    async with db_pool() as session:
        result = await session.execute(admins_sql_query)
        return [int(row[0]) for row in result]


async def init():
    global artists_ids, admins_ids
    admins_ids = await init_admins_ids()
    artists_ids = await init_artists_ids()


loop = asyncio.get_event_loop()
init_task = loop.create_task(init())
loop.run_until_complete(asyncio.wait([init_task]))

print(admins_ids, artists_ids)