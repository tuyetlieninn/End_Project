from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    # EmailStr tự động validate đúng định dạng email
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    # Đúng theo API仕様: FE mong nhận field tên idToken (không phải access_token)
    idToken: str


class UserRead(BaseModel):
    id: int
    email: str
    role: str
    model_config = {"from_attributes": True}