import os
from datetime import datetime, timedelta

from fastapi import status
from jose import JWTError, jwt

from src.schemas.base import MessageResponse

CONTACT_NOT_FOUND_MESSAGE = "Contact not found"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

responses = {
    status.HTTP_200_OK: {"model": MessageResponse},
    status.HTTP_400_BAD_REQUEST: {"model": MessageResponse},
    status.HTTP_401_UNAUTHORIZED: {"model": MessageResponse},
    status.HTTP_404_NOT_FOUND: {"model": MessageResponse},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageResponse},
}


def create_access_token(username: str):
    """Create an access token for the given username"""
    expire = datetime.utcnow() + timedelta(days=365)
    token = jwt.encode(
        {"sub": username, "exp": expire},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return token


def is_token_expired(token: str) -> bool:
    """Check if the given JWT token is expired"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = datetime.utcfromtimestamp(payload["exp"])
        current_time = datetime.utcnow()
        return current_time > expiration_time
    except JWTError:
        return True
