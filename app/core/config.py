from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Project Management API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite+aiosqlite:///./project.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
