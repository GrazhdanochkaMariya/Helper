from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.get_async_database_url()
    DATABASE_PARAMS = {"poolclass": NullPool}

    SYNC_DATABASE_URL = None
    SYNC_DATABASE_PARAMS = {}
else:
    DATABASE_URL = settings.get_async_database_url()
    DATABASE_PARAMS = {}

    SYNC_DATABASE_URL = settings.get_database_url()
    SYNC_DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Used only to initialize DB!!!
sync_session_maker = None
if SYNC_DATABASE_URL:
    sync_engine = create_engine(SYNC_DATABASE_URL, **SYNC_DATABASE_PARAMS)
    sync_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=sync_engine
    )


class Base(DeclarativeBase):
    pass
