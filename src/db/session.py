"""Module contains functions to create db connection"""
import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
HOSTNAME = os.getenv("POSTGRES_HOSTNAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DB}"

Base = declarative_base()

__engine = None

__async_session = None


def get_or_create_engine() -> AsyncEngine:
    """Creates and returns async engine"""
    global __engine
    if not __engine:
        __engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
    return __engine


def get_or_create_session() -> AsyncSession:
    """Creates and returns async session"""
    global __async_session
    if not __async_session:
        __async_session = sessionmaker(
            __engine, expire_on_commit=False, class_=AsyncSession
        )
    return __async_session()


async def dispose_engine():
    """Stops engine"""
    global __engine
    if __engine:
        await __engine.dispose()
    __engine = None
