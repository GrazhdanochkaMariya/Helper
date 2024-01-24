from collections.abc import AsyncGenerator
import datetime

import pytest
import pytest_asyncio
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.database import Base, get_db_session
from src.main import app
from src.models import TypeEnum, LeadContact


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    DATABASE_URL = settings.get_async_database_url()
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()

    contact_data_1 = get_contact_data()
    contact_1 = LeadContact(**contact_data_1)
    session.add(contact_1)
    await session.commit()

    contact_data_2 = get_contact_data()
    contact_2 = LeadContact(**contact_data_2)
    session.add(contact_2)
    await session.commit()

    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


def get_name() -> str:
    """Provides fake name for tests"""
    faker = Faker()

    return faker.name()


def get_contact_data(status_type = TypeEnum.CONTACT) -> dict:
    return {
        "lead_name": get_name(),
        "linkedin_profile": get_name(),
        "next_contact": f"{datetime.datetime.now()}",
        "status": status_type,
    }
