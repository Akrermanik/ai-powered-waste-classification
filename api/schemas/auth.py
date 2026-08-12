from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserInfo(BaseModel):
    id: int
    username: str
    name: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo
