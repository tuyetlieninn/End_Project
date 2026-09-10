from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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