from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
<<<<<<< HEAD
    app_name: str = "End Project API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./project.db"
    jwt_secret: str = "secret"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
=======
    # Đọc các giá trị này từ file .env (tạo ở bước sau)
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 ngày

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # lru_cache giúp chỉ đọc file .env 1 lần duy nhất, các lần gọi sau dùng lại kết quả cũ
    return Settings()
>>>>>>> develop
