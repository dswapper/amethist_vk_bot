from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.abstract import get_model_by_id_abstract

from bot.db.models import Orders


async def get_order_by_id(order_id: int, session: AsyncSession) -> Orders:
    return await get_model_by_id_abstract(order_id, session, Orders)