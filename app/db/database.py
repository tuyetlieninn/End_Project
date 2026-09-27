from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# the URL uses the async aiosqlite driver
SQLALCHEMY_DATABASE_URL = settings.database_url

# async engine so queries can be awaited
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()