from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.hash import argon2
from pydantic_settings import BaseSettings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db
import backend.models as models
import backend.services.auth as auth


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


# Helper: parse Authorization header and return token string
def extract_bearer_token(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    return authorization.split(" ", 1)[1]


# Concrete get_current_user dependency
async def get_current_user_from_header(authorization: str | None = None, db: AsyncSession = Depends(get_db)):
    token = extract_bearer_token(authorization)
    try:
        payload = jwt.decode(token, auth.settings.JWT_SECRET, algorithms=[auth.settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        token_version = int(payload.get("token_version", 0))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # fetch user and compare token_version
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.token_version != token_version:
        # token invalidated server-side (forced logout, password change, etc.)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    return user


# We'll provide a concrete implementation below in main.py that uses Authorization header,
# decodes access token, checks exp and token_version in DB, and returns User ORM object.
