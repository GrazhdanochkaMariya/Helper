import base64
import pdb
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pytest_mock import mocker
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from src.admin.auth import SessionAuth
from src.auth.auth import authenticate_user, create_access_token, swagger_login
from src.auth.dependencies import get_current_user
from src.database import async_session_maker
from src.main import app
from src.models import User
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

client = TestClient(app)


# @pytest.mark.asyncio
# async def test_swagger_login(db_session: AsyncSession):
#     credentials = HTTPBasicCredentials(username="masha@gmail.com", password="hashed_password")
#     response = client.post("/login", headers={"content-type": "application/x-www-form-urlencoded"}, data=credentials.__dict__)
#     assert response.status_code == 200

# @pytest.fixture
# def mock_request():
#     return MagicMock(spec=Request)
#
#
# @pytest.mark.asyncio
# async def test_login_successful(db_session: AsyncSession, mock_request):
#     form_data = {"username": "masha@gmail.com", "password": "hashed_password"}
#     mock_request.form = AsyncMock(return_value=form_data)
#     user_id = 1
#     authenticate_user.return_value = {"id": user_id}
#     access_token = "some-access-token"
#     create_access_token.return_value = access_token
#
#     result = await SessionAuth().login(mock_request)
#
#     assert result is True
#     mock_request.session.update.assert_called_once_with({"token": access_token})