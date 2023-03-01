from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor

kb_menu = Keyboard(inline=True)

kb_menu.add(Text('Заказать скин'), KeyboardButtonColor.POSITIVE)
kb_menu.row()
kb_menu.add(Text('Обратиться в поддержку'), KeyboardButtonColor.NEGATIVE)
kb_menu.row()
kb_menu.add(Text('Пойти нахуй'), KeyboardButtonColor.SECONDARY)
kb_menu = kb_menu.get_json()

labeler = BotLabeler()

@labeler.message(text="Привет")
async def start_handler(message: Message):
    user_info = await message.ctx_api.users.get(message.from_id)
    await message.answer(f'Привет, {user_info[0].first_name}! \n Чем могу помочь?', keyboard=kb_menu)

#TODO: админ панель где можно добавлять художников для распределния заказов + чат с художником + выбор модели и рефы