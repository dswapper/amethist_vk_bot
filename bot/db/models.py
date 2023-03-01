from sqlalchemy import Column, Integer, VARCHAR, Boolean

from bot.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class Artists(BaseModel):
    __tablename__ = "artists"

    peer_id = Column(Integer(), unique=True)
    is_artist = Column(Boolean())


class Admins(BaseModel):
    __tablename__ = "admins"

    peer_id = Column(Integer(), unique=True)
    is_admin = Column(Boolean())
