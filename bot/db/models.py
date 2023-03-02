import enum

from sqlalchemy import Column, Integer, Float, VARCHAR, Boolean, DateTime, Enum
from sqlalchemy import ForeignKey
from sqlalchemy import func

from bot.db.base import Base


class OrderType(enum.Enum):
    skin_air = 'air'
    skin_shady = 'shady'
    skin_century = 'century'
    totem_3d = 'totem3d'
    totem_2d = 'totem2d'


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class Artists(BaseModel):
    __tablename__ = "artists"

    peer_id = Column(Integer(), unique=True, nullable=False)
    is_artist = Column(Boolean())
    balance = Column(Float(), default=0)


class Admins(BaseModel):
    __tablename__ = "admins"

    peer_id = Column(Integer(), unique=True, nullable=False)
    is_admin = Column(Boolean())


class Users(BaseModel):
    __tablename__ = "users"

    balance = Column(Float(), default=0)


class Orders(BaseModel):
    __tablename__ = "orders"

    order_type = Column(Enum(OrderType))
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    ordered_at = Column(DateTime(timezone=True), server_default=func.now())

