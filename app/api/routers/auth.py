from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, Token, UserRead
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> Token:
    token = user_service.register(db, payload)
    return Token(idToken=token)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    token = user_service.login(db, payload)
    return Token(idToken=token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    # Route phụ để tự test middleware: gọi kèm token sẽ trả về thông tin user hiện tại
    return current_user