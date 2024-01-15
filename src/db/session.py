"""Module contains functions to create db connection"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

try:
    DB_PORT = int(DB_PORT)
except (ValueError, TypeError):
    raise ValueError("DB_PORT must be a valid integer")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()

__engine = None

__async_session = None


def get_or_create_engine() -> AsyncEngine:
    """Creates and returns async engine"""
    global __engine
    if not __engine:
        __engine = create_async_engine(DATABASE_URL, future=True)
    return __engine


def get_or_create_session() -> AsyncSession:
    """Creates and returns async session"""
    global __async_session
    if not __async_session:
        __async_session = sessionmaker(__engine, expire_on_commit=False, class_=AsyncSession)
    return __async_session()


async def dispose_engine():
    """Stops engine"""
    global __engine
    if __engine:
        await __engine.dispose()
    __engine = None
