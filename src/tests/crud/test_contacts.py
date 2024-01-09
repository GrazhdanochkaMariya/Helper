import pdb
from typing import AsyncGenerator

import pytest

from src.crud.contact import contact_crud


@pytest.mark.asyncio
async def test_get_contact_by_profile(add_contacts_to_db: tuple, prepare_database: AsyncGenerator):
    """Tests get playlist by filter"""
    profile_1, _ = add_contacts_to_db
    playlist = await contact_crud.get_contact_by_profile(prepare_database, profile_url=profile_1.linkedin_profile)
    pdb.set_trace()
    assert len(playlist) == 3