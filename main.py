import secrets

from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

from src.api.users import router as users_router
from src.api.auth import router as admin_auth
from src.api.transfer import router as transfer_router


app = FastAPI(
    title="FastAPI",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(users_router, prefix="/api", tags=["Contacts"])
app.include_router(admin_auth, prefix="/api/auth", tags=["Auth"])
app.include_router(transfer_router, prefix="/api", tags=["Transfer"])

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "AndersenLeads")
    correct_password = secrets.compare_digest(credentials.password, "eVxuw88jWpajhyJI")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)