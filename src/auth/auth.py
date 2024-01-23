from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.auth.dao import UserDAO
from src.config import settings
from src.models import User

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


async def authenticate_user(email: EmailStr, password: str) -> User:
    user = await UserDAO.select_one_or_none_filter_by(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
