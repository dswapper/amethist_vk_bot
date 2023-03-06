from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule, LevenshteinRule, StateRule
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.order_states import OrderStates
from bot.handlers.keyboard import *
from bot.handlers.state_dispenser import state_dispenser
from bot.enums import *

order_labeler = BotLabeler()


@order_labeler.message(CommandRule('cancel') | LevenshteinRule('отмена'))
async def cancel_handler(message: Message):
    try:
        await state_dispenser.delete(peer_id=message.from_id)
    except KeyError:
        pass
    await start_handler(message)


@order_labeler.message(LevenshteinRule('привет') | CommandRule('start'))
async def start_handler(message: Message):
    user_info = await message.ctx_api.users.get(message.from_id)
    await message.answer(f'Привет, {user_info[0].first_name}! \n Чем могу помочь?', keyboard=kb_start_menu)


@order_labeler.message(text=order_text)
async def start_order_handler(message: Message):
    await message.answer('Выбери что хочешь заказать: ', keyboard=kb_choosing_order_type)
    await state_dispenser.set(message.from_id, OrderStates.choosing_prod_type)


@order_labeler.message(StateRule(OrderStates.choosing_prod_type))
async def choosing_prod(message: Message):
    if message.text == product_totem_text:
        await message.answer('Тотем! Прекрасный выбор, ты хочешь 2D или 3D?', keyboard=kb_choosing_totem_type)
        await state_dispenser.set(message.from_id, OrderStates.choosing_totem_type)

    elif message.text == product_skin_text:
        await message.answer('Скин? Моделька Алекс или Стива?', keyboard=kb_choosing_skin_model)
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_model)

    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=choosing_prod)

        # await message.answer('А теперь опиши то, как ты видишь свой будующий скин и желательно, '
        #                      'чтобы ты прикрепил примерные изображения того, что хочешь получить,'
        #                      'когда всё пришлёшь, просто напиши мне /done и я отправлю всё художнику.')


@order_labeler.message(StateRule(OrderStates.choosing_skin_model))
async def choosing_skin_model(message: Message):
    if message.text == product_skin_normal:
        await message.answer('Ты выбрал модельку Стива')
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_style, skin_model=SkinModel.steve)
    elif message.text == product_skin_slim:
        await message.answer('Ты выбрал модельку Алекс')
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_style, skin_model=SkinModel.alex)
    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=kb_choosing_skin_model)
        return
    await message.answer('Отлично, в каком стиле будем рисовать?', keyboard=kb_choosing_skin_style)


@order_labeler.message(StateRule(OrderStates.choosing_skin_style))
async def choosing_skin_style(message: Message):
    if message.text == product_skin_air:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.air)
    elif message.text == product_skin_century:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.century)
    elif message.text == product_skin_shady:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.shady)
    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=kb_choosing_skin_style)