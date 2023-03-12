from vkbottle.bot import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Tuple

from bot.db.models import Users
from bot.enums.roles import Roles
from .labelers import get_admin_role_autorule, get_artist_role_autorule
from .labelers import artist_labeler, admin_labeler
from bot.utils.users import register_user

admin_labeler.auto_rules = get_admin_role_autorule(admin_labeler)
artist_labeler.auto_rules = get_artist_role_autorule(artist_labeler)


@admin_labeler.message(command='setrole')
async def wrong_amount_args_set_role_handler(message: Message) -> None:
    await message.answer('Вы ввели слишком много или слишком мало аргументов. \n Формат команды: /setrole @nick role')


@admin_labeler.message(command=('setrole', 2))
async def set_role_handler(message: Message, args: Tuple[str],
                           session: AsyncSession) -> None:
    try:
        vk_id = int(args[0].split('|')[0].replace('[id', ''))  # @mention or int id
        arg_role = args[1]
        new_role = Roles.role_admin if arg_role == 'admin' else Roles.role_artist \
            if arg_role == 'artist' else Roles.role_user if arg_role == 'user' else None
        if arg_role is None:
            await message.answer('Вы ввели неправильную роль (доступные роли: admin, user, artist)')
            return
    except ValueError:
        await message.answer('Неправильный аргумент, пришлите id или @nick пользователя и желаемую роль в формате '
                             'admin, user, artist')
    else:
        await register_user(vk_id, session)
        async with session:
            update_user_sql_query = update(Users).values(role=new_role).where(Users.vk_id == vk_id)
            await session.execute(update_user_sql_query)
            await session.commit()
            await message.answer(f'Роль пользователя {vk_id} успешно обновлена!')

    artist_labeler.auto_rules = get_artist_role_autorule(artist_labeler)
    admin_labeler.auto_rules = get_admin_role_autorule(admin_labeler)

# TODO: FSM and keyboard
