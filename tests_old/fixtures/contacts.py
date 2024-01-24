import datetime

import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TypeEnum, LeadContact


def get_name() -> str:
    """Provides fake name for tests"""
    faker = Faker()

    return faker.name()


def get_contact_data() -> dict:
    return {
        "lead_name": get_name(),
        "linkedin_profile": get_name(),
        "next_contact": f"{datetime.datetime.now()}",
        "status": TypeEnum.CONTACT,
    }


@pytest_asyncio.fixture
async def add_contacts_to_db(session: AsyncSession) -> tuple:
    """Add contacts to db for tests"""
    contact_data_1 = get_contact_data()
    contact_1 = LeadContact(**contact_data_1)
    session.add(contact_1)
    await session.commit()

    contact_data_2 = get_contact_data()
    contact_2 = LeadContact(**contact_data_2)
    session.add(contact_2)
    await session.commit()

    return contact_1, contact_2
