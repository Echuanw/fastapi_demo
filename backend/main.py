from datetime import datetime, timedelta
from uuid import uuid4

import auth
from database import Base, engine, get_db
from fastapi import Cookie, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
import models
import schemas
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn


# create tables (for demo only; use Alembic in real projects)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(on_startup=[init_models])

# configure CORS
FRONTEND_ORIGIN = "http://localhost:3000"  # adjust to your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# POST /api/login
@app.post("/api/login", response_model=schemas.TokenResponse)
async def login(data: schemas.LoginRequest, response: Response, request: Request, db: AsyncSession = Depends(get_db)):
    # fetch user
    res = await db.execute(select(models.User).where(models.User.username == data.username))
    user = res.scalars().first()
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    # create access token
    access_token = auth.create_access_token(user.id, user.token_version)
    # create refresh token (jti saved in DB)
    refresh_jti = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(days=auth.settings.REFRESH_TOKEN_EXPIRES_DAYS)
    refresh_jwt = auth.create_refresh_token_jwt(refresh_jti, user.id, expires_at)

    # persist refresh token record
    token_row = models.RefreshToken(
        jti=refresh_jti,
        user_id=user.id,
        revoked=False,
        expires_at=expires_at,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(token_row)
    await db.commit()

    # set httpOnly cookie for refresh token
    # 注意：Secure=True 在开发 localhost http 下会导致 cookie 不被设置，生产必须 True。
    response.set_cookie(
        key="refresh_token",
        value=refresh_jwt,
        httponly=True,
        secure=False,  # 本地调试设 False，生产置 True
        samesite="lax",
        path="/api/refresh",
        expires=auth.settings.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 3600,
    )

    return {"access_token": access_token, "expires_in": auth.settings.ACCESS_TOKEN_EXPIRES_SECONDS}


# POST /api/refresh
@app.post("/api/refresh", response_model=schemas.TokenResponse)
async def refresh(
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_db),
    refresh_token: str | None = Cookie(None),
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    # decode refresh JWT to get jti and user
    try:
        payload = jwt.decode(refresh_token, auth.settings.JWT_SECRET, algorithms=[auth.settings.JWT_ALGORITHM])
        jti = payload.get("jti")
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # lookup refresh token in DB
    res = await db.execute(select(models.RefreshToken).where(models.RefreshToken.jti == jti))
    token_row = res.scalars().first()
    if not token_row:
        # unknown token -> possible attack
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")
    if token_row.revoked:
        # reuse of revoked token -> possible token leak; revoke all user's refresh tokens
        await db.execute(
            update(models.RefreshToken).where(models.RefreshToken.user_id == token_row.user_id).values(revoked=True)
        )
        await db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
    if token_row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # rotation: create new refresh jti, mark old revoked and replaced_by_jti
    new_jti = str(uuid4())
    new_expires = datetime.utcnow() + timedelta(days=auth.settings.REFRESH_TOKEN_EXPIRES_DAYS)
    new_refresh_jwt = auth.create_refresh_token_jwt(new_jti, token_row.user_id, new_expires)
    # insert new token row and mark old revoked
    new_token_row = models.RefreshToken(
        jti=new_jti,
        user_id=token_row.user_id,
        revoked=False,
        expires_at=new_expires,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(new_token_row)
    # update old
    await db.execute(
        update(models.RefreshToken)
        .where(models.RefreshToken.id == token_row.id)
        .values(revoked=True, replaced_by_jti=new_jti)
    )
    await db.commit()

    # issue new access token
    res_user = await db.execute(select(models.User).where(models.User.id == token_row.user_id))
    user = res_user.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = auth.create_access_token(user.id, user.token_version)

    # set rotated refresh cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_jwt,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/api/refresh",
        expires=auth.settings.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 3600,
    )
    return {"access_token": access_token, "expires_in": auth.settings.ACCESS_TOKEN_EXPIRES_SECONDS}


# POST /api/logout
@app.post("/api/logout")
async def logout(response: Response, refresh_token: str | None = Cookie(None), db: AsyncSession = Depends(get_db)):
    if refresh_token:
        # try decode and revoke that jti
        try:
            payload = jwt.decode(refresh_token, auth.settings.JWT_SECRET, algorithms=[auth.settings.JWT_ALGORITHM])
            jti = payload.get("jti")
            await db.execute(update(models.RefreshToken).where(models.RefreshToken.jti == jti).values(revoked=True))
            await db.commit()
        except JWTError:
            pass
    # clear cookie
    response.delete_cookie(key="refresh_token", path="/api/refresh")
    return {"msg": "logged out"}


# protected: GET /api/me
@app.get("/api/me", response_model=schemas.UserOut)
async def me(current_user: models.User = Depends(get_current_user_from_header)):
    # current_user is an ORM object; Pydantic orm_mode will convert fields
    return current_user


def main():
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
