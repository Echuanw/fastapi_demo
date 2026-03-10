# 专门处理 token 生成、校验、刷新等
from datetime import datetime, timedelta, timezone
import hashlib
import os
import secrets    # 生成 refresh_token
import uuid

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.hash import argon2
from pydantic_settings import BaseSettings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
import app.models as models


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRES_DAYS: int = 14


settings = Settings(JWT_SECRET=os.getenv("SECRET_KEY"))


def verify_password(plain: str, hashed: str) -> bool:
    return argon2.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return argon2.hash(password)


def get_uuid(token: str) -> str:
    return uuid.uuid5(uuid.NAMESPACE_DNS, token)


# create access token
def create_access_token(user_id: int) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(user_id),  # 用户ID
        "iat": now,  # 签发时间
        "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES_SECONDS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


# create_refresh_token
def create_refresh_token(user_id: int, ip: str) -> tuple[str, datetime, int]:
    """
    生成 refresh token（opaque string）
    """
    # 生成随机部分
    random_part = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRES_DAYS),)
    # 拼接 secret 信息
    secret = f"{user_id}:{ip}:{str(expires_at)}:{random_part}"
    # 明文 token（客户端存）
    refresh_token = hashlib.sha256(secret.encode()).hexdigest() + random_part
    # 存数据库的 hash（安全）
    token_hash = get_password_hash(refresh_token.encode()) # noqa: F841
    token_uuid = get_uuid(refresh_token)  # noqa: F841
    return (refresh_token, expires_at, settings.REFRESH_TOKEN_EXPIRES_DAYS,)


# verify_access_token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


# async def get_current_user_jti(user_id) -> Optional[uuid.UUID]:
#     """
#     从 Authorization header 解析 access_token，获取 refresh_token 的 jti
#     """
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="缺少或无效的token")
#     token = auth_header.split(" ")[1]
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         refresh_jti = payload.get("refresh_jti")
#         if not refresh_jti:
#             raise HTTPException(status_code=401, detail="token缺少jti")
#         return UUID(refresh_jti)
#     except JWTError:
#         raise HTTPException(status_code=401, detail="token无效")


# Helper: parse Authorization header and return access token string
def extract_bearer_token(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    return authorization.split(" ", 1)[1]


# Concrete get_current_user dependency
async def get_current_user_from_header(authorization: str | None = "bearer", db: AsyncSession = Depends(get_db)):
    token = extract_bearer_token(authorization)
    try:
        payload = verify_token(token)
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # fetch user and compare token_version
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# We'll provide a concrete implementation below in main.py that uses Authorization header,
# decodes access token, checks exp and token_version in DB, and returns User ORM object.
