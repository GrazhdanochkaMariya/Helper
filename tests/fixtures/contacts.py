import datetime

import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.old.models import Contact, TypeEnum


async def get_name() -> str:
    """Provides fake name for tests"""
    faker = Faker()

    return faker.name()


async def get_contact_data() -> dict:
    return {
        "lead_name": await get_name(),
        "linkedin_profile": await get_name(),
        "next_contact": f"{datetime.datetime.now()}",
        "status": TypeEnum.CONTACT,
    }


@pytest_asyncio.fixture
async def add_contacts_to_db(prepare_database: AsyncSession) -> tuple:
    """Add contacts to db for tests"""
    contact_data_1 = await get_contact_data()
    contact_1 = Contact(**contact_data_1)
    prepare_database.add(contact_1)
    await prepare_database.commit()

    contact_data_2 = await get_contact_data()
    contact_2 = Contact(**contact_data_2)
    prepare_database.add(contact_2)
    await prepare_database.commit()

    return contact_1, contact_2