import json
import secrets
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.auth import router as admin_auth
from src.api.transfer import router as transfer_router
from src.api.users import router as users_router
from src.crud.auth import admin_crud
from src.db.db import get_db
from src.db.session import dispose_engine, get_or_create_engine
from src.session_storage import create_session
from src.utils import create_access_token, is_token_expired

app = FastAPI(
    title="FastAPI",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(users_router, prefix="/api", tags=["Contacts"])
app.include_router(admin_auth, prefix="/api/auth", tags=["Auth"])
app.include_router(transfer_router, prefix="/api", tags=["Transfer"])


@app.on_event("startup")
async def startup():
    """Starts engine on apps run"""
    get_or_create_engine()


@app.on_event("shutdown")
async def shutdown():
    """Stops engine on apps stop"""
    await dispose_engine()


security = HTTPBasic()
db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def get_current_username(
        db: db_dependency,
        credentials: HTTPBasicCredentials = Depends(security),
):
    """Authenticate user and get current username"""
    correct_username = secrets.compare_digest(credentials.username, "AndersenLeads")
    correct_password = secrets.compare_digest(credentials.password, "eVxuw88jWpajhyJI")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    admin = await admin_crud.get_admin(
        db=db,
        username=credentials.username,
        password=credentials.password
    )
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin does not exist"
        )
    new_token = create_access_token(credentials.username)

    if not admin.token:
        await admin_crud.update_admin_token(
            db=db,
            admin_id=admin.id,
            new_token=new_token
        )
    else:
        is_expired = is_token_expired(token=admin.token)

        if is_expired:
            await admin_crud.update_admin_token(
                db=db,
                admin_id=admin.id,
                new_token=new_token
            )
        else:
            new_token = admin.token

    return credentials.username, new_token


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(auth_data=Depends(get_current_username)):
    """Get Swagger documentation"""
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    session_id = str(uuid.uuid4())
    await create_session(username=auth_data[0], session_id=session_id)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    response.set_cookie(key="user_token", value=auth_data[1], httponly=True)
    return response


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(auth_data=Depends(get_current_username)):
    """Get ReDoc documentation"""
    response = get_redoc_html(openapi_url="/openapi.json", title="docs")
    session_id = str(uuid.uuid4())
    await create_session(username=auth_data[0], session_id=session_id)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    response.set_cookie(key="user_token", value=auth_data[1], httponly=True)
    return response


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    """Get OpenAPI documentation"""
    openapi_spec = get_openapi(title=app.title, version=app.version, routes=app.routes)
    response = Response(content=json.dumps(openapi_spec))
    response.headers["Content-Type"] = "application/json"
    return response
