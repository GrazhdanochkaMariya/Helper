from typing import Any

from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse

from src.admin.auth import authentication_backend
from src.admin.views import LeadContactAdmin, UserAdmin
from src.api.router import router as api_router
from src.auth.auth import swagger_login
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
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=settings.MODE == 'production',
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(LeadContactAdmin)


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(_: Any = Depends(swagger_login)) -> HTMLResponse:
    """Get Swagger documentation"""
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    return response


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(_: Any = Depends(swagger_login)) -> HTMLResponse:
    """Get ReDoc documentation"""
    response = get_redoc_html(openapi_url="/openapi.json", title="docs")
    return response


@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: Any = Depends(swagger_login)) -> JSONResponse:
    """Get OpenAPI documentation"""
    return JSONResponse(app.openapi())


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api", tags=["API"])
