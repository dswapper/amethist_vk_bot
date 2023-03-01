from vkbottle.bot import BotLabeler, Message, rules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Tuple

from bot.db.models import Admins
from bot.db.init_roles import admins_ids


admin_labeler = BotLabeler()
user_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(admins_ids)]


@admin_labeler.message(command = ('addadmin', 1))
async def add_admin_handler(message: Message, args: Tuple[str], session: AsyncSession):
    peer_id = args[0].split('|')[0].replace('[id', '')
    try:
        peer_id = int(peer_id)
    except:
        await message.answer('Неправильный аргумент, нужно прислать id в формате @nick или цифрами')
    else:
        new_admin = Admins()
        new_admin.peer_id = peer_id
        new_admin.is_admin = True
        try:
            session.add(new_admin)
            await session.commit()
        except IntegrityError:
            await message.answer(f'Пользователь уже имеет роль Администратор')
        else:
            await message.answer(f'Пользователь {peer_id} успешно добавлен!')



@admin_labeler.message(command='check')
async def check_handler(message: Message):
    await message.answer('Вы админ!')


@user_labeler.message(command='check')
async def check_handler_user(message: Message):
    await message.answer('Вы не админ и не художник!')