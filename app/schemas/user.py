import re

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password_strength(value: str) -> str:
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least 1 digit")
    return value


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


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
