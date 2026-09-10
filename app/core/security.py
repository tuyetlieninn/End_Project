from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


def hash_password(plain: str) -> str:
    # Chuyển: chuỗi -> bytes -> hash bằng bcrypt -> chuyển lại thành chuỗi
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    # So sánh mật khẩu nhập vào với hash đã lưu trong DB
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(email: str, role: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    # payload chứa email + role để FE decode được { email, role } như API仕様 yêu cầu
    payload = {"sub": email, "email": email, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    settings = get_settings()
    # Nếu token sai/hết hạn, jwt.decode sẽ tự raise lỗi (InvalidTokenError)
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])