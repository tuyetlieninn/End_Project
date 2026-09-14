from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.database import engine

# async_sessionmaker thay cho sessionmaker — tạo ra AsyncSession thay vì Session thường
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    # "async def" + "async with" thay cho try/finally thường
    # Khi FastAPI dùng xong sẽ tự động await để đóng session
    async with SessionLocal() as db:
        yield db