from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from src.crud.auth import admin_crud
from src.db.db import get_db
from src.session_storage import validate_session
from src.utils import responses, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.post("/token")
async def login_for_access_token(
        db: db_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await admin_crud.get_admin(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(
        token: str = Cookie(None,  include_in_schema=False),
        session_id: str = Cookie(None,  include_in_schema=False)

):

    if token is None and session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token and session provided",
        )
    if token is not None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            return {"message": "You are authorized"}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    result = await validate_session(session_id)
    if result:
        return {"message": "You are authorized"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )


@router.post("/", responses=responses)
async def create_user(
        db: db_dependency,
        username: str,
        password: str
):
    data = {
        "username": username,
        "password": password
    }
    check_name = await admin_crud.check_admin_name(db=db, username=username)
    if check_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already registered in db")

    user = await admin_crud.create_admin(db=db, data=data)
    return user
