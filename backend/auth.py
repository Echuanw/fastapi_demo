from datetime import datetime, timedelta

from database import get_db
from fastapi import Depends
from jose import jwt
from passlib.hash import argon2
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRES_DAYS: int = 14

    class Config:
        env_file = ".env"


settings = Settings()


def verify_password(plain: str, hashed: str) -> bool:
    return argon2.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return argon2.hash(password)


def create_access_token(user_id: int, token_version: int) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES_SECONDS),
        "token_version": token_version,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token_jwt(jti: str, user_id: int, expires_at: datetime) -> str:
    payload = {"sub": str(user_id), "jti": jti, "iat": datetime.utcnow(), "exp": expires_at}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(authorization: str | None = None, db: AsyncSession = Depends(get_db)):
    # This dependency expects Authorization header "Bearer <token>"

    # using Header here convenient: but FastAPI will supply None if missing
    # to get header: pass parameter as authorization: str = Header(None)
    # For clarity, expect calling as Depends(get_current_user) from routes where header exists.
    raise RuntimeError("请在 main.py 中通过 Depends(get_current_user_from_header) 使用具体实现")


# We'll provide a concrete implementation below in main.py that uses Authorization header,
# decodes access token, checks exp and token_version in DB, and returns User ORM object.
