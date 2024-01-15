"""Module contains base fixtures for tests"""
import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import DB_USER, DB_PASS, TEST_DB_HOST, TEST_DB_PORT, TEST_DB_NAME
from main import app
from src.db.db import get_db
from src.db.session import Base

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = DATABASE_URL_TEST


async def override_get_async_session() -> AsyncGenerator:
    """Returns session"""
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_database() -> AsyncGenerator:
    """Creates, returns f=db for tests and drops it after tests finish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Returns async client"""
    async with AsyncClient(app=app, base_url="https://test") as ac:
        yield ac
