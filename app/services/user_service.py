from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def register(db: AsyncSession, payload: RegisterRequest) -> User:
    if await get_user_by_email(db, payload.email) is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="member",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user  # trả về User, không trả token nữa


async def login(db: AsyncSession, payload: LoginRequest) -> User:
    user = await get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user  # trả về User, không trả token nữa