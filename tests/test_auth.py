import pytest
from fastapi import HTTPException
from fastapi.security import  HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.auth.auth import authenticate_user, create_access_token, swagger_login
from src.auth.dependencies import get_current_user

from tests.conftest import get_user_data


@pytest.mark.asyncio
async def test_authenticate_user(db_session: AsyncSession, mocker):
    mocker.patch("src.auth.auth.verify_password", return_value=True)
    authenticated_user = await authenticate_user("any@email.com", "password", db_session)
    assert authenticated_user

    wrong_user = await authenticate_user("test@example.com", "wrong_password", db_session)
    assert not wrong_user


@pytest.mark.asyncio
async def test_get_current_user(db_session: AsyncSession):
    token = create_access_token({"sub": str(1)})
    current_user = await get_current_user(token, db_session)
    assert current_user.id == 1

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid_token", db_session)
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_swagger_login_with_valid_credentials(mocker, db_session: AsyncSession):
    mock_request = mocker.MagicMock(spec=Request)
    user_data = get_user_data()
    credentials = HTTPBasicCredentials(username=user_data['email'], password=user_data['hashed_password'])

    mock_request.headers = {"Authorization": f"Basic {credentials.username}:{credentials.password}"}
    mock_request.session = {}
    mocker.patch("src.auth.auth.verify_password", return_value=True)

    await swagger_login(mock_request, credentials=credentials, session=db_session)

    assert "token" in mock_request.session


@pytest.mark.asyncio
async def test_swagger_login_with_invalid_credentials(mocker, db_session: AsyncSession):
    mock_request = mocker.MagicMock(spec=Request)
    credentials = HTTPBasicCredentials(username="invalid_name", password="invalid_password")

    mock_request.headers = {"Authorization": f"Basic {credentials.username}:{credentials.password}"}
    mock_request.session = {}
    mocker.patch("src.auth.auth.verify_password", return_value=True)

    with pytest.raises(HTTPException) as exc_info:
        await swagger_login(mock_request, credentials=credentials, session=db_session)
    assert exc_info.value.status_code == 401

