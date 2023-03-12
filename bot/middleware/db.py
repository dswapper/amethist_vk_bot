from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from bot.db.base import db_pool


class DbSessionMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        self.session_pool = db_pool

        async with self.session_pool() as session:
            self.send({'session': session})
