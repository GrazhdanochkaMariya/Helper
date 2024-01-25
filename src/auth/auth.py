from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.config import settings
from src.dao.user_dao import UserDAO
from src.database import get_db_session
from src.models import User


security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_access_token_for_headers(
    data: dict
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(
        email: EmailStr,
        password: str,
        session: AsyncSession,
) -> User:
    user = await UserDAO(session).select_one_or_none_filter_by(email=email)
    if user and verify_password(password, user.hashed_password):
        return user


async def swagger_login(
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
        session: AsyncSession = Depends(get_db_session),
):
    """Authenticate user and get token"""
    user = await authenticate_user(str(credentials.username), str(credentials.password), session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    request.session.update({"token": access_token})
