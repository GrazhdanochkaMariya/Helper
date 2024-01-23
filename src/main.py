import json

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqladmin import Admin
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src.admin.auth import authentication_backend
from src.admin.views import LeadContactAdmin, UserAdmin
from src.api.router import router as api_router
from src.auth.auth import create_access_token, authenticate_user
from src.config import app_configs, settings
from src.database import engine

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(LeadContactAdmin)

security = HTTPBasic()


async def swagger_login(
        credentials: HTTPBasicCredentials = Depends(security),
):
    """Authenticate user and get token"""
    user = await authenticate_user(str(credentials.username), str(credentials.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    new_token = create_access_token({"sub": str(user.id)})
    return new_token


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(auth_data=Depends(swagger_login)):
    """Get Swagger documentation"""
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(key="token", value=auth_data, httponly=True)
    return response


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(auth_data=Depends(swagger_login)):
    """Get ReDoc documentation"""
    response = get_redoc_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(key="token", value=auth_data, httponly=True)
    return response


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(swagger_login)):
    """Get OpenAPI documentation"""
    openapi_spec = get_openapi(title=app.title, version=app.version, routes=app.routes)
    response = Response(content=json.dumps(openapi_spec))
    response.headers["Content-Type"] = "application/json"
    return response



@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api", tags=["API"])
