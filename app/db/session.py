from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.database import engine

# factory for AsyncSession objects
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    # one session per request; closed automatically when the request ends
    async with SessionLocal() as db:
        yield db