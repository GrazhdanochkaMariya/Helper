"""Module contains base fixtures for tests"""
import asyncio
from typing import AsyncGenerator, Callable

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from src.auth.dependencies import get_current_user
from src.config import settings
from src.database import Base, async_session

from src.main import app
from src.models import User

engine = create_async_engine(
    settings.get_async_test_database_url(),
    poolclass=StaticPool,
)
test_async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator:
    """Returns session"""
    async with test_async_session() as session:
        yield session

app.dependency_overrides[async_session] = session


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    """Creates, returns f=db for tests and drops it after tests finish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)



@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Returns async client"""
    async with AsyncClient(app=app, base_url="https://test") as ac:
        yield ac


async def mock_get_user() -> User:
    return User(
        id=1,
        email="masha@gmail.com",
        hashed_password="hashed_password"
    )


@pytest_asyncio.fixture
async def get_mock_user() -> Callable:
    return mock_get_user


@pytest_asyncio.fixture
async def auth_fixture(get_mock_user) -> Callable:
    app.dependency_overrides[get_current_user] = get_mock_user
    yield get_mock_user
    app.dependency_overrides[get_current_user] = get_current_user

@pytest_asyncio.fixture(scope="session")
async def event_loop() -> AsyncGenerator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()