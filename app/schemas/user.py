from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


def validate_password_strength(value: str) -> str:
    # Kiểm tra thêm ngoài min_length: phải có ít nhất 1 chữ hoa, 1 chữ thường, 1 số
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least 1 digit")
    return value


class RegisterRequest(BaseModel):
    email: EmailStr

    password: str = Field(min_length=8, max_length=128)


    # field_validator chạy SAU khi Field(min_length=8) đã pass, kiểm tra thêm điều kiện phức tạp
    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class LoginRequest(BaseModel):
    email: EmailStr
    role: str
    created_at: datetime


class Token(BaseModel):
    idToken: str
    user: UserInfo


class UserRead(BaseModel):
    id: int
    email: str
    role: str
    model_config = {"from_attributes": True}