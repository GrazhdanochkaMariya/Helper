import datetime
from typing import AsyncGenerator

import pytest

from src.crud.contact import contact_crud
from src.models.users import TypeEnum


@pytest.mark.asyncio
async def test_get_contact_by_profile(
        add_contacts_to_db: tuple,
        prepare_database: AsyncGenerator
):
    """Tests get contact by profile"""
    contact = await contact_crud.get_contact_by_profile(prepare_database,
                                                        linkedin_profile=
                                                        add_contacts_to_db[0].linkedin_profile)
    assert contact.lead_name == add_contacts_to_db[0].lead_name


@pytest.mark.asyncio
async def test_delete_contact_by_profile(
        add_contacts_to_db: tuple,
        prepare_database: AsyncGenerator
):
    """Tests delete contact"""
    await contact_crud.delete_contact_by_profile(
        prepare_database,
        linkedin_profile=add_contacts_to_db[0].linkedin_profile
    )
    contact_deleted = await contact_crud.get_contact_by_profile(prepare_database,
                                                                linkedin_profile=
                                                                add_contacts_to_db[0].linkedin_profile
                                                                )
    contact_existing = await contact_crud.get_contact_by_profile(
        prepare_database,
        linkedin_profile=
        add_contacts_to_db[1].linkedin_profile
    )

    assert contact_existing
    assert not contact_deleted


@pytest.mark.asyncio
async def test_get_contacts(
        prepare_database: AsyncGenerator,
        add_contacts_to_db: tuple
):
    """Test getting all contacts"""
    contacts = await contact_crud.get_contacts(db=prepare_database)

    assert len(contacts) == 2


@pytest.mark.asyncio
async def test_update_contact(
        prepare_database: AsyncGenerator,
        add_contacts_to_db: tuple
):
    """Test updating a contact"""
    new_data = {"lead_name": "Updated Name"}
    await contact_crud.update_contact(
        db=prepare_database,
        new_data=new_data,
        contact_id=add_contacts_to_db[0].id
    )
    updated_contact = await contact_crud.get_contact_by_profile(
        prepare_database,
        linkedin_profile=add_contacts_to_db[0].linkedin_profile
    )

    assert updated_contact.lead_name == "Updated Name"


@pytest.mark.asyncio
async def test_create_contact(prepare_database: AsyncGenerator):
    """Test creating a new contact"""
    new_contact_data = {
        "lead_name": "New Contact",
        "linkedin_profile": "linkedin/profile",
        "next_contact": datetime.datetime.now(),
        "status": TypeEnum.CONTACT
    }
    new_contact = await contact_crud.create_contact(
        db=prepare_database,
        new_data=new_contact_data
    )

    assert new_contact.lead_name == new_contact_data["lead_name"]
    assert new_contact.linkedin_profile == new_contact_data["linkedin_profile"]
    assert new_contact.next_contact == new_contact_data["next_contact"]
    assert new_contact.status == new_contact_data["status"]


@pytest.mark.asyncio
async def test_update_contact_status(
        prepare_database: AsyncGenerator,
        add_contacts_to_db: tuple
):
    """Test updating contact status"""
    await contact_crud.update_contact_status(
        db=prepare_database,
        new_status=TypeEnum.DECLINED,
        contact_id=add_contacts_to_db[0].id
    )
    updated_contact = await contact_crud.get_contact_by_profile(
        prepare_database,
        linkedin_profile=add_contacts_to_db[0].linkedin_profile
    )
    assert updated_contact.status == TypeEnum.DECLINED
