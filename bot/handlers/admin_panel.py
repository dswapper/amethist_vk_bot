from vkbottle.bot import BotLabeler, Message, rules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Tuple

from bot.db.models import Users
from bot.db.get_roles import get_roles
from bot.enums.roles import Roles


admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(get_roles()['admins_list'])]


@admin_labeler.message(command='setrole')
async def wrong_amount_args_set_role_handler(message: Message):
    await message.answer('Вы ввели слишком много или слишком мало аргументов. \n Формат команды: /setrole @nick role')


@admin_labeler.message(command=('setrole', 2))
async def set_role_handler(message: Message, args: Tuple[str], session: AsyncSession):
    try:
        peer_id = int(args[0].split('|')[0].replace('[id', '')) # @mention or int id
        arg_role = args[1]
        new_role = Roles.role_admin if arg_role == 'admin' else Roles.role_artist \
            if arg_role == 'artist' else Roles.role_user

    except ValueError:
        await message.answer('Неправильный аргумент, пришлите id или @nick пользователя и желаемую роль в формате admin user artist')
    else:
        get_user_sql_query = select(Users).limit(1).where(Users.peer_id == peer_id)
        async with session:
            result = [item for item in await session.execute(get_user_sql_query)]
            if len(result) != 0:
                update_user_sql_query = update(Users).values(role=new_role).where(Users.peer_id == peer_id)
                await session.execute(update_user_sql_query)
                await session.commit()
                await message.answer(f'Роль пользователя {peer_id} успешно обновлена!')
            else:
                new_user = Users()
                new_user.peer_id = peer_id
                new_user.role = new_role
                session.add(new_user)
                await session.commit()
                await message.answer(f'Пользователь был успешно добавлен в базу данных и ему была установленна роль!')


# TODO FSM and keyboard
