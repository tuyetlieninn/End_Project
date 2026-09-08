from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    # Tìm user theo email, trả về None nếu không có
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def register(db: Session, payload: RegisterRequest) -> str:
    # Email trùng thì báo lỗi 409 (Conflict)
    if get_user_by_email(db, payload.email) is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="member",  # user tự đăng ký luôn là member, không phải admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Đăng ký xong tự tạo luôn token để auto-login, đúng API仕様
    return create_access_token(user.email, user.role)


def login(db: Session, payload: LoginRequest) -> str:
    user = get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return create_access_token(user.email, user.role)