import pdb
from typing import AsyncGenerator

import pytest

from src.crud.contact import contact_crud


@pytest.mark.asyncio
async def test_get_contact_by_profile(add_contacts_to_db: tuple, prepare_database: AsyncGenerator):
    """Tests get contact by profile"""
    profile_1, _ = add_contacts_to_db
    contact = await contact_crud.get_contact_by_profile(prepare_database, linkedin_profile=profile_1.linkedin_profile)
    assert contact.lead_name == profile_1.lead_name