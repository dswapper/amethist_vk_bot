from sqlalchemy import Column, Integer, Float, VARCHAR, Boolean, DateTime, Enum
from sqlalchemy import ForeignKey
from sqlalchemy import func

from bot.db.base import Base
from bot.enums import *


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class Users(BaseModel):
    __tablename__ = "users"

    vk_id = Column(Integer(), unique=True, nullable=False)
    balance = Column(Float(), default=0)
    role = Column(Enum(Roles))


class Orders(BaseModel):
    __tablename__ = "orders"

    order_type = Column(Enum(OrderType))
    skin_style = Column(Enum(SkinStyle))
    skin_model = Column(Enum(SkinModel))
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    ordered_at = Column(DateTime(timezone=True), server_default=func.now())


class ReferenceMessage(BaseModel):
    __tablename__ = 'ref_msgs'

    order_id = Column(Integer(), ForeignKey('orders.id'))
    message_id = Column(Integer())


class ArtistPriority(BaseModel):
    __tablename__ = 'artist_priority'

    artist_id = Column(Integer(), ForeignKey('users.id'))
    priority = Column(Float())
