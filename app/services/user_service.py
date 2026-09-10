from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)  # execute cần await
    return result.scalars().first()


async def register(db: AsyncSession, payload: RegisterRequest) -> str:
    if await get_user_by_email(db, payload.email) is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="member",
    )
    db.add(user)
    await db.commit()       # commit cần await
    await db.refresh(user)  # refresh cần await

    return create_access_token(user.email, user.role)


async def login(db: AsyncSession, payload: LoginRequest) -> str:
    user = await get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return create_access_token(user.email, user.role)