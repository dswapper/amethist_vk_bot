from vkbottle.bot import BotLabeler, Message, MessageMin
from vkbottle.dispatch.rules.base import CommandRule, LevenshteinRule, StateRule
from sqlalchemy.ext.asyncio import AsyncSession

from copy import copy
from typing import List
from random import randint

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
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_model, msg=[])

    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=choosing_prod)


@order_labeler.message(StateRule(OrderStates.choosing_skin_model))
async def choosing_skin_model(message: Message):
    if message.text == product_skin_normal:
        await message.answer('Ты выбрал модельку Стива')
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_style, skin_model=SkinModel.steve,
                                  msg=message.state_peer.payload['msg'])
    elif message.text == product_skin_slim:
        await message.answer('Ты выбрал модельку Алекс')
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_style, skin_model=SkinModel.alex,
                                  msg=message.state_peer.payload['msg'])
    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=kb_choosing_skin_model)
        return
    await message.answer('Отлично, в каком стиле будем рисовать?', keyboard=kb_choosing_skin_style)


@order_labeler.message(StateRule(OrderStates.choosing_skin_style))
async def choosing_skin_style(message: Message):
    if message.text == product_skin_air:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.air,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    elif message.text == product_skin_century:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.century,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    elif message.text == product_skin_shady:
        await state_dispenser.set(message.from_id, OrderStates.sending_references, skin_style=SkinStyle.shady,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=kb_choosing_skin_style)
        return
    await message.answer('А теперь опиши то, как ты видишь свой будующий скин и желательно, '
                         'чтобы ты прикрепил примерные изображения того, что хочешь получить,'
                         'когда всё пришлёшь, просто напиши мне /done и я отправлю всё художнику.')


@order_labeler.message(CommandRule('done') & StateRule(OrderStates.sending_references))
async def sending_references_done_handler(message: Message):
    msg_list : List[MessageMin]
    msg_list = message.state_peer.payload['msg']
    if len(msg_list) == 0:
        await message.answer('Похоже ты ничего не отправил...')
    else:
        await message.answer('Отлично! А теперь перед тем как я отправлю сообщение художнику, тебе нужно будет оплатить '
                             'его работу. Просто нажми на кнопку под окном для сообщений и оплати свой заказ.', keyboard=kb_pay)

        art_msg = f"Вам пришёл заказ от пользователя {message.from_id}. " \
                  f"\nМодель скина: {message.state_peer.payload['skin_model']}" \
                  f"\nСтиль скина: {message.state_peer.payload['skin_style']}" \
                  f"\nПользователь отправил следующие пожелания:"

        await message.ctx_api.messages.send(user_id=215115154, random_id=randint(0,20000000), message=art_msg)

        for msg in msg_list:
            await message.ctx_api.messages.send(user_id=215115154, random_id=randint(0,20000000), message=msg.text,
                                                attachment=','.join(msg.get_attachment_strings()))

        await state_dispenser.delete(message.from_id)


@order_labeler.message(StateRule(OrderStates.sending_references))
async def sending_references_handler(message: Message):
    prev_msg = message.state_peer.payload['msg']
    msg = list(copy(prev_msg))
    msg.append(message)
    await state_dispenser.set(message.from_id, OrderStates.sending_references,
                              skin_model=message.state_peer.payload['skin_model'],
                              skin_style=message.state_peer.payload['skin_style'],
                              msg=msg)

# TODO: с заказом приходит тип модельки + забивается в базу данных + выбор художника + чек оплаты
