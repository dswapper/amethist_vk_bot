from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule, LevenshteinRule
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.order_states import OrderStates
from bot.handlers.keyboard import *
from bot.handlers.state_dispenser import state_dispenser

order_labeler = BotLabeler()


@order_labeler.message(CommandRule('cancel') | LevenshteinRule('отмена'))
async def cancel_handler(message: Message):
    await state_dispenser.delete(peer_id=message.from_id)
    await start_handler(message)


@order_labeler.message(LevenshteinRule('привет') | CommandRule('start'))
async def start_handler(message: Message):
    user_info = await message.ctx_api.users.get(message.from_id)
    await message.answer(f'Привет, {user_info[0].first_name}! \n Чем могу помочь?', keyboard=kb_start_menu)


@order_labeler.message(text=order_text)
async def order_handler(message: Message, session: AsyncSession):
    await message.answer('Выбери что хочешь заказать: ', keyboard=kb_choosing_order_type)
    await state_dispenser.set(message.from_id, OrderStates.choosing_prod_type)

# TODO: админ панель где можно добавлять художников для распределния заказов + чат с художником + выбор модели и рефы
