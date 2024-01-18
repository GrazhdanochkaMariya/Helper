import pytest
from httpx import AsyncClient
from starlette import status

from src.tests.fixtures.contacts import get_name
from src.utils import CONTACT_NOT_FOUND_MESSAGE


async def get_contact_data(status_type: str) -> dict:
    return {
        "lead_name": await get_name(),
        "linkedin_profile": await get_name(),
        "next_contact": "06.04.2024",
        "status": status_type,
    }


@pytest.mark.asyncio
async def test_get_contact_success(client: AsyncClient, add_contacts_to_db: tuple):
    response = await client.get("/api/check/contact",
                                params={
                                    "linkedin_profile":
                                        add_contacts_to_db[0].linkedin_profile
                                })
    contact = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert contact["lead_name"] == add_contacts_to_db[0].lead_name


@pytest.mark.asyncio
async def test_get_contact_fail(client: AsyncClient):
    response = await client.get("/api/check/contact",
                                params={"linkedin_profile": "invalid/profile"})
    contact = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert contact["detail"] == CONTACT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_delete_contact_success(client: AsyncClient, add_contacts_to_db: tuple):
    response = await client.delete("/api/delete/contact",
                                   params={
                                       "linkedin_profile":
                                           add_contacts_to_db[0].linkedin_profile
                                   })
    deleted_contact = response.json()

    check_contact = await client.get("/api/check/contact",
                                     params={
                                         "linkedin_profile":
                                             add_contacts_to_db[0].linkedin_profile
                                     })

    assert response.status_code == status.HTTP_200_OK
    assert deleted_contact
    assert check_contact.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_contact_fail(client: AsyncClient):
    response = await client.delete("/api/delete/contact",
                                   params={"linkedin_profile": "invalid/profile"})
    deleted_contact = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert deleted_contact["detail"] == CONTACT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_contact_status(client: AsyncClient):
    data = await get_contact_data(status_type="contact")
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data_response["linkedin_profile"] == data["linkedin_profile"]


@pytest.mark.asyncio
async def test_process_google_sheets_exist_contact_status(
        client: AsyncClient,
        add_contacts_to_db: tuple
):
    data = await get_contact_data(status_type="contact")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data_response


@pytest.mark.asyncio
async def test_process_google_sheets_exist_declined_status(
        client: AsyncClient,
        add_contacts_to_db: tuple
):
    data = await get_contact_data(status_type="declined")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data_response


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_declined_status(client: AsyncClient):
    data = await get_contact_data(status_type="declined")
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data_response["detail"] == CONTACT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_process_google_sheets_exist_dnm_status(
        client: AsyncClient,
        add_contacts_to_db: tuple
):
    data = await get_contact_data(status_type="dnm")
    data["linkedin_profile"] = add_contacts_to_db[0].linkedin_profile
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data_response


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_declined_status(client: AsyncClient):
    data = await get_contact_data(status_type="declined")
    response = await client.post("/api/update/contact",
                                 json=data)
    data_response = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data_response["detail"] == CONTACT_NOT_FOUND_MESSAGE
