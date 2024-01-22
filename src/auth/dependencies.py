from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from src.auth.dao import UserDAO
from src.config import settings
from src.exceptions import (IncorrectTokenException, TokenAbsentException,
                            TokenExpiredException, UserIsNotPresentException)
from src.models import User


def get_token(request: Request):
    token = request.headers.get("authentication")
    if not token:
        raise TokenAbsentException()
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenException()
    # Check token expiration
    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()
    # Check if the token and user match
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException()
    # Check if user is present in database
    user = await UserDAO.select_one_or_none_filter_by(id=int(user_id))
    if not user:
        raise UserIsNotPresentException()

    return user
