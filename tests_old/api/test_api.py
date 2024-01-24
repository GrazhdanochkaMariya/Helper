from typing import Callable

import pytest
from httpx import AsyncClient
from starlette import status

from src.api.dao import LeadContactDAO
from src.utils import CONTACT_NOT_FOUND_MESSAGE
from tests.fixtures.contacts import get_name


def get_contact_data(status_type: str) -> dict:
    return {
        "lead_name": get_name(),
        "linkedin_profile": get_name(),
        "next_contact": "06.04.2024",
        "status": status_type,
    }


@pytest.mark.asyncio
async def test_get_contact_success(client: AsyncClient, add_contacts_to_db: tuple):
    response = await client.get(
        "/api/check/contact/",
        params={"linkedin_profile": add_contacts_to_db[0].linkedin_profile},
    )
    contact = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert contact["lead_name"] == add_contacts_to_db[0].lead_name


@pytest.mark.asyncio
async def test_get_contact_fail(client: AsyncClient):
    response = await client.get(
        "/api/check/contact/", params={"linkedin_profile": "invalid/profile"}
    )
    contact = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert contact["detail"] == CONTACT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_contact_status_401(
        client: AsyncClient
):
    data = get_contact_data(status_type="contact")
    response = await client.post("/api/gs/changed", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_contact_status(client: AsyncClient, auth_fixture: Callable):
    data = get_contact_data(status_type="contact")
    response = await client.post("/api/gs/changed", json=data)

    new_contact = await LeadContactDAO.select_one_or_none_filter_by(
        linkedin_profile=data["linkedin_profile"]
    )
    assert response.status_code == status.HTTP_200_OK
    assert new_contact.linkedin_profile == data["linkedin_profile"]


@pytest.mark.asyncio
async def test_process_google_sheets_exist_contact_status(
        client: AsyncClient, add_contacts_to_db: tuple, auth_fixture: Callable
):
    data = get_contact_data(status_type="contact")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/gs/changed", json=data)
    contact = await LeadContactDAO.select_one_or_none_filter_by(
        linkedin_profile=add_contacts_to_db[0].linkedin_profile)

    assert response.status_code == status.HTTP_200_OK
    assert contact.status == data["status"].upper()


@pytest.mark.asyncio
async def test_process_google_sheets_exist_declined_status(
        client: AsyncClient, add_contacts_to_db: tuple, auth_fixture: Callable
):
    data = get_contact_data(status_type="declined")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/gs/changed", json=data)
    contact = await LeadContactDAO.select_one_or_none_filter_by(
        linkedin_profile=add_contacts_to_db[0].linkedin_profile)

    assert response.status_code == status.HTTP_200_OK
    assert not contact


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_declined_status(client: AsyncClient, auth_fixture: Callable):
    data = get_contact_data(status_type="declined")
    response = await client.post("/api/gs/changed", json=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_process_google_sheets_exist_dnm_status(
        client: AsyncClient, add_contacts_to_db: tuple, auth_fixture: Callable
):
    data = get_contact_data(status_type="dnm")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/gs/changed", json=data)
    contact = await LeadContactDAO.select_one_or_none_filter_by(
        linkedin_profile=add_contacts_to_db[0].linkedin_profile)

    assert response.status_code == status.HTTP_200_OK
    assert contact.status == data["status"].upper()
