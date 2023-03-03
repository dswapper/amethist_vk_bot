from vkbottle.bot import BotLabeler, Message, rules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Tuple

from bot.db.models import Admins, Artists
from bot.db.init_roles import admins_ids, artists_ids


admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(admins_ids)]


@admin_labeler.message(command = ('addadmin', 1))
async def add_admin_handler(message: Message, args: Tuple[str], session: AsyncSession):
    peer_id = args[0].split('|')[0].replace('[id', '')
    try:
        peer_id = int(peer_id)
    except KeyError:
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
            admins_ids.append(peer_id)
            await message.answer(f'Пользователь {peer_id} успешно получил роль Администратор!')


@admin_labeler.message(command = ('addartist', 1))
async def add_artist_handler(message: Message, args: Tuple[str], session: AsyncSession):
    peer_id = args[0].split('|')[0].replace('[id', '')
    try:
        peer_id = int(peer_id)
    except:
        await message.answer('Неправильный аргумент, нужно прислать id в формате @nick или цифрами')
    else:
        new_artist = Artists()
        new_artist.peer_id = peer_id
        new_artist.is_artist = True
        try:
            session.add(new_artist)
            await session.commit()
        except IntegrityError:
            await message.answer(f'Пользователь уже имеет роль Художник')
        else:
            artists_ids.append(peer_id)
            await message.answer(f'Пользователь {peer_id} успешно получил роль Художник!')
