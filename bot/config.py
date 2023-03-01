import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    VK_TOKEN = os.environ.get('VK_TOKEN')
    DEBUG_MODE = os.environ.get('DEBUG_MODE')
    DATABASE_URL = "postgresql+asyncpg://postgres:postgrespw@localhost:32768"
    if DEBUG_MODE:
        DATABASE_URL = "postgresql+asyncpg://postgres:postgrespw@localhost:32768"
    else:
        DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql+asyncpg://')