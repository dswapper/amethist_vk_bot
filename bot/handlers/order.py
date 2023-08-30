from vkbottle.bot import Message, MessageMin
from vkbottle.dispatch.rules.base import CommandRule, LevenshteinRule, StateRule
from sqlalchemy.ext.asyncio import AsyncSession

from copy import copy
from typing import List
from random import randint

from bot.handlers.states.order_states import OrderStates
from bot.handlers.view import *
from bot.handlers.states.state_dispenser import state_dispenser
from bot.enums import *
from bot.utils.users import register_user
from bot.db.models import ReferenceMessage, Orders, Users
from bot.utils.users import get_user_by_vkid
from bot.utils.orders import get_order_by_id
from bot.handlers.view.pictures_urls import air_style_pic_url, shady_style_pic_url, century_style_pic_url

from .labelers import order_labeler


@order_labeler.message(CommandRule('cancel') | LevenshteinRule('отмена'))
async def cancel_handler(message: Message, session: AsyncSession) -> None:
    try:
        await state_dispenser.delete(peer_id=message.from_id)
    except KeyError:
        pass
    await start_handler(message, session)


@order_labeler.message(LevenshteinRule('привет') | CommandRule('start'))
async def start_handler(message: Message, session: AsyncSession) -> None:
    user_info = await message.ctx_api.users.get(message.from_id)
    await message.answer(f'Привет, {user_info[0].first_name}! \n Чем могу помочь?', keyboard=kb_start_menu)
    await register_user(message.from_id, session=session)


@order_labeler.message(text=order_text)
async def start_order_handler(message: Message) -> None:
    await message.answer('Выбери что хочешь заказать: ', keyboard=kb_choosing_order_type)
    await state_dispenser.set(message.from_id, OrderStates.choosing_prod_type)


@order_labeler.message(StateRule(OrderStates.choosing_prod_type))
async def choosing_prod(message: Message) -> None:
    if message.text == product_totem_text:
        await message.answer('Тотем! Прекрасный выбор, ты хочешь 2D или 3D?', keyboard=kb_choosing_totem_type)
        await state_dispenser.set(message.from_id, OrderStates.choosing_totem_type)

    elif message.text == product_skin_text:
        await message.answer('Скин? Моделька Алекс или Стива?', keyboard=kb_choosing_skin_model)
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_model, msg=[])

    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=choosing_prod)


@order_labeler.message(StateRule(OrderStates.choosing_skin_model))
async def choosing_skin_model(message: Message) -> None:
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
    await message.answer('Отлично, посмотри в каких стилях мы рисуем и выбери понравившийся!', keyboard=kb_choosing_skin_style)


@order_labeler.message(StateRule(OrderStates.choosing_skin_style))
async def choosing_skin_style(message: Message) -> None:
    if message.text == product_skin_air:
        await message.answer("Это стиль Air", attachment=air_style_pic_url, keyboard=kb_next_n_back)
        await state_dispenser.set(message.from_id, OrderStates.confirming_skin_style, skin_style=SkinStyle.air,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    elif message.text == product_skin_century:
        await message.answer("Это стиль Century", attachment=century_style_pic_url, keyboard=kb_next_n_back)
        await state_dispenser.set(message.from_id, OrderStates.confirming_skin_style, skin_style=SkinStyle.century,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    elif message.text == product_skin_shady:
        await message.answer("Это стиль Shady", attachment=shady_style_pic_url, keyboard=kb_next_n_back)
        await state_dispenser.set(message.from_id, OrderStates.confirming_skin_style, skin_style=SkinStyle.shady,
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
    else:
        await message.answer('Похоже ты выбрал что-то не то, попробуй снова', keyboard=kb_choosing_skin_style)
        return


@order_labeler.message(StateRule(OrderStates.confirming_skin_style))
async def confirming_skin_style_handler(message: Message) -> None:
    if message.text == next_msg:
        await state_dispenser.set(message.from_id, OrderStates.sending_references,
                                  skin_style=message.state_peer.payload['skin_style'],
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])
        await message.answer('А теперь опиши то, как ты видишь свой будущий скин и желательно, '
                             'чтобы ты прикрепил примерные изображения того, что хочешь получить,'
                             'когда всё пришлёшь, просто напиши мне /done и я отправлю всё художнику.')
    else:
        await message.answer('Отлично, посмотри в каких стилях мы рисуем и выбери понравившийся!',
                             keyboard=kb_choosing_skin_style)
        await state_dispenser.set(message.from_id, OrderStates.choosing_skin_style,
                                  skin_style=message.state_peer.payload['skin_style'],
                                  skin_model=message.state_peer.payload['skin_model'],
                                  msg=message.state_peer.payload['msg'])


@order_labeler.message(CommandRule('done') & StateRule(OrderStates.sending_references))  # TODO: Refactoring
async def sending_references_done_handler(message: Message, session: AsyncSession) -> None:
    await register_user(message.from_id, session)
    user: Users = await get_user_by_vkid(message.from_id, session)
    msg_list: List[MessageMin]
    msg_list = message.state_peer.payload['msg']
    if len(msg_list) == 0:
        await message.answer('Похоже ты ничего не отправил...')
    else:
        await message.answer('Отлично! А теперь перед тем как я отправлю сообщение художнику, '
                             'тебе нужно будет оплатить его работу. '
                             'Просто нажми на кнопку под окном для сообщений и оплати свой заказ.', keyboard=kb_pay)

        async with session:
            new_order = Orders()
            new_order.order_status = OrderStatus.user_send_references
            new_order.order_type = OrderType.skin
            new_order.user_id = user.id
            new_order.skin_model = message.state_peer.payload['skin_model']
            new_order.skin_style = message.state_peer.payload['skin_style']
            new_order.cost = 160  # TODO: система смены цены

            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)

            order_id = new_order.id

        order: Orders = await get_order_by_id(order_id, session)
        art_msg = f"Вам пришёл заказ от пользователя {user.vk_id} / Внутренний id для связи: {user.id}. " \
                  f"\nМодель скина: {order.skin_model}" \
                  f"\nСтиль скина: {order.skin_style}" \
                  f"\nПользователь отправил следующие пожелания:"

        await message.ctx_api.messages.send(user_id=533880207, random_id=randint(0,20000000), message=art_msg)
        # TODO: Выбор художника + только после оплаты

        for msg in msg_list:
            attachment = ','.join(msg.get_attachment_strings())
        #     await message.ctx_api.messages.send(user_id=533880207, random_id=randint(0,20000000), message=msg.text,
        #                                         attachment=attachment)
            async with session:
                new_ref_msg = ReferenceMessage()
                new_ref_msg.order_id = order_id
                new_ref_msg.message_text = msg.text
                new_ref_msg.message_attachments = attachment

                session.add(new_ref_msg)
                await session.commit()

        await state_dispenser.delete(message.from_id)


@order_labeler.message(StateRule(OrderStates.sending_references))
async def sending_references_handler(message: Message) -> None:
    prev_msg = message.state_peer.payload['msg']
    msg = list(copy(prev_msg))
    msg.append(message)
    await state_dispenser.set(message.from_id, OrderStates.sending_references,
                              skin_model=message.state_peer.payload['skin_model'],
                              skin_style=message.state_peer.payload['skin_style'],
                              msg=msg)


# TODO: с заказом приходит тип модельки + забивается в базу данных + выбор художника + чек оплаты + пользователь в БД
# TODO: перед выбором стиля показывать картиночку
# TODO: тесты
# TODO: все тексты в отдельный файл для удобного редактирования (через .format)
# TODO: сообщения художнику refactor
