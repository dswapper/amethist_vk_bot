from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()


@labeler.message(text='ping8')
async def echo_handler(message: Message):
    await message.reply("pong!")
