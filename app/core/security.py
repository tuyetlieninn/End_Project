from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings

MAX_PASSWORD_BYTES = 72  # bcrypt input limit


def hash_password(plain: str) -> str:
    
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    password = plain.encode("utf-8")
    # Registration rejects passwords over the bcrypt limit, so a longer one can
    # never match; bcrypt would raise instead of returning False.
    if len(password) > MAX_PASSWORD_BYTES:
        return False
    return bcrypt.checkpw(password, hashed.encode("utf-8"))


def create_access_token(email: str, role: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": email, "email": email, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])