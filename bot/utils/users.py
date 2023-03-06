from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models import Users


async def get_user_vkid(user_id: int, session: AsyncSession):
    sql_query = select(Users.vk_id).limit(1).where(Users.id == user_id)
    async with session:
        result = [item for item in await session.execute(sql_query)]
        if len(result) != 1:
            return None
        else:
            return result[0][0]