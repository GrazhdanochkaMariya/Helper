import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.dao.lead_contact_dao import LeadContactDAO
from src.models import TypeEnum
from src.utils import CONTACT_NOT_FOUND_MESSAGE
from tests.conftest import get_contact_data


@pytest.mark.asyncio
async def test_sync_gs_midnight_sanity_check(client: AsyncClient):
    # prepare test data
    data = {
        "lead_name": "test",
        "linkedin_profile": "test",
        "next_contact": "2021-10-11",
        "status": "contact",
    }
    response = await client.post("/api/gs/changed", json=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_contact_success(client: AsyncClient, db_session: AsyncSession):
    # prepare test data
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    await LeadContactDAO(db_session).create_contact(data)

    response = await client.get(
        "/api/check/contact/",
        params={"linkedin_profile": data["linkedin_profile"]},
    )
    contact = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert contact["lead_name"] == data["lead_name"]


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
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    response = await client.post("/api/gs/changed", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_contact_status(
        client: AsyncClient,
        db_session: AsyncSession,
):
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    response = await client.post("/api/gs/changed", json=data)

    new_contact = await LeadContactDAO(db_session).select_one_or_none_filter_by(
        linkedin_profile=data["linkedin_profile"]
    )
    assert response.status_code == status.HTTP_200_OK
    assert new_contact.linkedin_profile == data["linkedin_profile"]


@pytest.mark.asyncio
async def test_process_google_sheets_exist_contact_status(
        client: AsyncClient,
        db_session: AsyncSession,
):
    # prepare test data
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    await LeadContactDAO(db_session).create_contact(data)

    data_changed = get_contact_data(status_type="contact")
    data_changed["linkedin_profile"] = data["linkedin_profile"]
    response = await client.post("/api/gs/changed", json=data_changed)
    contact = await LeadContactDAO(db_session).select_one_or_none_filter_by(
        linkedin_profile=data["linkedin_profile"])

    assert response.status_code == status.HTTP_200_OK
    assert contact.status == data["status"].upper()


@pytest.mark.asyncio
async def test_process_google_sheets_exist_declined_status(
        client: AsyncClient,
        db_session: AsyncSession,
):
    # prepare test data
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    await LeadContactDAO(db_session).create_contact(data)

    data["status"] = TypeEnum.DECLINED
    response = await client.post("/api/gs/changed", json=data)

    # validate result
    contact = await LeadContactDAO(db_session).select_one_or_none_filter_by(
        linkedin_profile=data["linkedin_profile"])

    assert response.status_code == status.HTTP_200_OK
    assert not contact


@pytest.mark.asyncio
async def test_process_google_sheets_non_exist_declined_status(client: AsyncClient):
    data = get_contact_data(status_type=TypeEnum.DECLINED)
    response = await client.post("/api/gs/changed", json=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_process_google_sheets_exist_dnm_status(
        client: AsyncClient,
        db_session: AsyncSession,
):
    # prepare test data
    data = get_contact_data(status_type=TypeEnum.CONTACT)
    await LeadContactDAO(db_session).create_contact(data)

    data["status"] = TypeEnum.DNM
    response = await client.post("/api/gs/changed", json=data)

    # validate result
    contact = await LeadContactDAO(db_session).select_one_or_none_filter_by(
        linkedin_profile=data["linkedin_profile"])

    assert response.status_code == status.HTTP_200_OK
    assert contact.status == data["status"].upper()
