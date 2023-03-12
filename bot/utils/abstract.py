from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models import BaseModel


async def get_model_by_param_abstract(id: int, session: AsyncSession, model: BaseModel, param: Any) -> BaseModel:
    sql_query = select(model).limit(1).where(param == id)
    async with session:
        result = [item for item in await session.execute(sql_query)]
        if len(result) != 1:
            return None
        else:
            return result[0][0]


async def get_model_by_id_abstract(id: int, session: AsyncSession, model: BaseModel):
    return await get_model_by_param_abstract(id, session, model, model.id)
