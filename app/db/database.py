from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./end_project.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
