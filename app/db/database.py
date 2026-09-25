from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# driver "aiosqlite" thay cho driver sync mặc định của SQLite
SQLALCHEMY_DATABASE_URL = settings.database_url

# create_async_engine thay cho create_engine — cho phép query bất đồng bộ (await)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Base vẫn giữ nguyên, không đổi
Base = declarative_base()