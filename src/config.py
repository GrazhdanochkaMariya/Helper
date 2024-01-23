from typing import Any, List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Andersen Marketing Lead Helper Project API"
    app_summary: str = "TODO"
    app_description: str = "TODO"

    # SECRET KEY IS USED FOR SECURING AUTH
    SECRET_KEY: str
    ALGORITHM: str

    # STARTUP MODE
    # e.g. PRODUCTION, DEBUG, TEST
    MODE: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database settings
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str = ""
    CORS_HEADERS: list[str]

    # INITIAL SETUP
    FIRST_SUPERUSER: str = ""
    FIRST_SUPERUSER_PASSWORD: str = ""

    def get_database_url(self):
        database_url = (
            f"postgresql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return database_url

    def get_async_database_url(self):
        database_url = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return database_url


settings = Settings()

app_configs: dict[str, Any] = {
    "title": settings.app_name,
    "summary": settings.app_summary,
    "description": settings.app_description,
    "docs_url": None,
    "redoc_url": None,
    "openapi_url": None,
}
