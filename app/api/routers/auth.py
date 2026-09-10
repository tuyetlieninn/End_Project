from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, Token, UserInfo, UserRead
from app.services import user_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest, db: AsyncSession = Depends(get_db)
) -> Token:
    user = await user_service.register(db, payload)
    token = create_access_token(user.email, user.role)
    return Token(idToken=token, user=UserInfo(email=user.email, role=user.role))


@router.post("/login", response_model=Token)
async def login(
    payload: LoginRequest, db: AsyncSession = Depends(get_db)
) -> Token:
    user = await user_service.login(db, payload)
    token = create_access_token(user.email, user.role)
    return Token(idToken=token, user=UserInfo(email=user.email, role=user.role))


@router.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user
