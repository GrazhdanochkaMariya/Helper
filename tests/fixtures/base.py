"""Module contains base fixtures for tests"""
import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from app.main import app
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import DB_PASS, DB_USER, TEST_DB_HOST, TEST_DB_NAME, TEST_DB_PORT
from src.old.api.auth import get_current_user
from src.old.db import Base
from src.old.db.db import get_db

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = DATABASE_URL_TEST


async def override_get_async_session() -> AsyncGenerator:
    """Returns session"""
    async with async_session() as session:
        yield session


async def override_get_current_user(token: str = None, session_id: str = None):
    """Returns current user"""

    if token == "valid_token":
        return {"message": "You are authorized"}
    elif session_id == "valid_session_id":
        return {"message": "You are authorized"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )


app.dependency_overrides[get_db] = override_get_async_session
app.dependency_overrides[get_current_user] = override_get_async_session


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
