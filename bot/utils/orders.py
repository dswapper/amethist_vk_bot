from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from bot.utils.abstract import get_model_by_id_abstract, get_models_by_param_abstract
from bot.db.models import Orders, ReferenceMessage


async def get_order_by_id(order_id: int, session: AsyncSession) -> Orders:
    return await get_model_by_id_abstract(order_id, session, Orders)


async def get_reference_msgs_by_order_id(order_id: int, session: AsyncSession) -> List[ReferenceMessage]:
    return await get_models_by_param_abstract(order_id, session, ReferenceMessage, ReferenceMessage.order_id)