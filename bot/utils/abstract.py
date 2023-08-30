from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models import BaseModel


async def get_models_by_param_abstract(id_: int, session: AsyncSession, model: BaseModel, param: Any) -> List[BaseModel]:
    sql_query = select(model).limit(255).where(param == id_)
    async with session:
        result = await session.execute(sql_query)
        result = result.scalars().all()
        if len(result) == 0:
            return None
        else:
            return result


async def get_model_by_param_abstract(id_: int, session: AsyncSession, model: BaseModel, param: Any) -> BaseModel:
    result = await get_models_by_param_abstract(id_, session, model, param)
    return result[0]


async def get_model_by_id_abstract(id: int, session: AsyncSession, model: BaseModel):
    return await get_model_by_param_abstract(id, session, model, model.id)
