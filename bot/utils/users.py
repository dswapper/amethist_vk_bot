from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models import Users
from bot.enums.roles import Roles

from bot.utils.abstract import get_model_by_id_abstract, get_model_by_param_abstract

from loguru import logger


async def get_user_by_id(user_id: int, session: AsyncSession) -> Users:
    return await get_model_by_id_abstract(user_id, session, Users)


async def get_user_by_vkid(vk_id: int, session: AsyncSession) -> Users:
    return await get_model_by_param_abstract(vk_id, session, Users, Users.vk_id)


async def register_user(vk_id: int, session: AsyncSession):
    user: Users = await get_user_by_vkid(vk_id, session)
    if user is None:
        new_user = Users()
        new_user.vk_id = vk_id
        new_user.role = Roles.role_user
        async with session:
            session.add(new_user)
            await session.commit()
        logger.debug(f'User {vk_id} registered successfully')
        return new_user
    else:
        logger.debug(f'User {vk_id} has already registered')
        return None
