from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from bot.config import Config

engine = create_async_engine(Config.DATABASE_URL, future=True, echo=True)
engine_sync = create_engine(Config.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://'))
Base = declarative_base()

db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
db_sync_pool = sessionmaker(engine_sync)




