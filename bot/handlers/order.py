from vkbottle.bot import BotLabeler, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.keyboard import *


labeler = BotLabeler()


@labeler.message(lev='привет')
async def start_handler(message: Message):
    user_info = await message.ctx_api.users.get(message.from_id)
    await message.answer(f'Привет, {user_info[0].first_name}! \n Чем могу помочь?', keyboard=kb_start_menu)


@labeler.message(text=order_text)
async def order_handler(message: Message, session: AsyncSession):
    await message.answer('Выбери что хочешь заказать: ', keyboard=kb_choosing_order_type)

# TODO: админ панель где можно добавлять художников для распределния заказов + чат с художником + выбор модели и рефы
