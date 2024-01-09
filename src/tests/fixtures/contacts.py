import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import TypeEnum, Contact


async def get_name() -> str:
    """Provides fake name for tests"""
    faker = Faker()

    return faker.name()

async def get_contact_data() -> dict:
    return {
        "lead_name": get_name(),
        "lead_company": get_name(),
        "linkedin_profile": get_name(),
        "contact": get_name(),
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

    return contact_data_1, contact_data_2