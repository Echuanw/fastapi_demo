from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str | None = None  # 若支持 refresh token 旋转则返回新 token


class UserRegisterRequest(LoginRequest):
    email: EmailStr


# 响应体
class UserRegisterResponse(BaseModel):
    id: int
    created_at: datetime


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="客户端持有的 refresh token")


class RefreshTokenResponse(LoginResponse):
    pass


class RevokeRefreshTokenRequest(BaseModel):
    refresh_token: str


class RevokeRefreshTokenResponse(BaseModel):
    revoked: bool
    message: str | None = None


class UserOut(BaseModel):
    id: int
    email: str
    username: str | None = None
    role: str
    is_email_verified: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class LogoutRequest(BaseModel):
    refresh_jti: UUID


class LogoutResponse(BaseModel):
    message: str
