from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "End Project API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./project.db"
    jwt_secret: str = "secret"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
