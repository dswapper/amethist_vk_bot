from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import asyncio

from bot.config import Config

print('goat!')

engine = create_async_engine(Config.DATABASE_URL, future=True, echo=True)
Base = declarative_base()

db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



