from typing import AsyncGenerator

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings


DATABASE_URL = settings.get_async_database_url()
DATABASE_PARAMS = {}

SYNC_DATABASE_URL = settings.get_database_url()
SYNC_DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise e


# Used only to initialize DB!!!
sync_session_maker = None
if SYNC_DATABASE_URL:
    sync_engine = create_engine(SYNC_DATABASE_URL, **SYNC_DATABASE_PARAMS)
    sync_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=sync_engine
    )


class Base(DeclarativeBase):
    pass
