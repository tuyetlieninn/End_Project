import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.security import MAX_PASSWORD_BYTES


def validate_password_strength(value: str) -> str:
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least 1 digit")
    # bcrypt only accepts up to 72 bytes; longer input makes hashing raise (500)
    if len(value.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError(f"Password must be at most {MAX_PASSWORD_BYTES} bytes")
    return value


def normalize_email(value: str) -> str:
    # Emails are case-insensitive in practice: "Case@x.com" and "case@x.com" are one account
    return value.strip().lower()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("email")
    @classmethod
    def lower_email(cls, value: str) -> str:
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def lower_email(cls, value: str) -> str:
        return normalize_email(value)


class UserInfo(BaseModel):
    email: str
    role: str


class Token(BaseModel):
    idToken: str
    user: UserInfo


class UserRead(BaseModel):
    id: int
    email: str
    role: str
    model_config = {"from_attributes": True}