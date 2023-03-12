import enum


class OrderType(enum.Enum):
    skin = 'skin'
    totem_3d = 'totem3d'
    totem_2d = 'totem2d'


class SkinStyle(enum.Enum):
    air = 'air'
    century = 'century'
    shady = 'shady'


class SkinModel(enum.Enum):
    steve = 'steve'
    alex = 'alex'
