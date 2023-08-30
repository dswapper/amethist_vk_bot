from vkbottle.bot import Message
from sqlalchemy.ext.asyncio import AsyncSession

from random import randint
from typing import Tuple, List

from bot.utils.users import get_user_by_id
from bot.db.models import ReferenceMessage
from bot.utils.orders import get_reference_msgs_by_order_id
from .labelers import artist_labeler


@artist_labeler.message(command=('user', 1))
async def send_to_user_handler(message: Message, args: Tuple[str], session: AsyncSession) -> None:
    user = await get_user_by_id(int(args[0]), session)
    user_id = user.vk_id
    if user_id is None:
        await message.answer('Пользователь не найден, попробуйте снова')
    else:
        try:
            if len(message.fwd_messages) > 0:
                for msg in message.fwd_messages:
                    await message.ctx_api.messages.send(user_id=user_id, message=msg.text,
                                                        attachment=','.join(msg.get_attachment_strings()),
                                                        random_id=randint(0, 20000000))
            elif message.reply_message is not None:
                msg = message.reply_message
                await message.ctx_api.messages.send(user_id=user_id, message=msg.text,
                                                    attachment=','.join(msg.get_attachment_strings()),
                                                    random_id=randint(0, 20000000))
            else:
                await message.answer('Чтобы отправить сообщение клиенту,'
                                     ' перешли мне сообщение, которое хочешь отправить')
        except:
            await message.answer('Похоже что-то пошло не так, '
                                 'убедитесь что в пересылаемом сообщении нет других вложений кроме картинок')


# TODO: система очереди и выбора художника


@artist_labeler.message(command=('getref', 1))
async def get_references_by_order_id_handler(message: Message, args: Tuple[str], session: AsyncSession):
    order_id = int(args[0])
    ref_list: List[ReferenceMessage] = await get_reference_msgs_by_order_id(order_id, session)

    for msg in ref_list:
        await message.answer(message=msg.message_text, attachment=msg.message_attachments)