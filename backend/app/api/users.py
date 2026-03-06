import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.models import RefreshToken, User
from app.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RevokeRefreshTokenRequest,
    RevokeRefreshTokenResponse,
    UserOut,
    UserRegisterRequest,
    UserRegisterResponse,
)
from backend.services.token_service import (
    create_access_token,
    create_refresh_token,
    get_current_user_from_header,
    get_password_hash,
    get_uuid,
    verify_password,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # 可能有多个IP，取第一个
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.headers.get("x-real-ip", request.client.host)
    return ip


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user_from_header), session: AsyncSession = Depends(get_db)):
    # 查询用户及其 profile
    result = await session.execute(
        select(User).where(User.id == current_user.id, User.is_deleted == False)  # noqa: E712
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # 查询用户
    result = await db.execute(
        select(User).where(User.username == req.username, User.is_deleted == False)  # noqa: E712
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=400, detail="邮箱或密码错误")

    # 生成 access_token
    access_token = create_access_token(user.id)
    # 生成 refresh_token
    host_ip = get_client_ip(request)
    refresh_token, expires_at = create_refresh_token(user.id, host_ip)

    # 存储 refresh_token 的哈希
    new_refresh = RefreshToken(
        user_id=user.id,
        token_hash=get_password_hash(refresh_token),
        jti=get_uuid(refresh_token),
        expires_at=expires_at,
        is_revoked=False,
        created_ip=host_ip,
        user_agent=request.headers.get("user-agent", ""),
    )
    db.add(new_refresh)
    await db.commit()

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# @router.post("/logout", response_model=LogoutResponse)
# async def logout(
#     request: LogoutRequest,
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     注销接口：将 refresh_token 标记为已注销
#     """
#     refresh_jti = await get_current_user_jti(request)

#     # 查找 refresh_token
#     stmt = select(RefreshToken).where(RefreshToken.jti == refresh_jti)
#     result = await db.execute(stmt)
#     refresh_token = result.scalar_one_or_none()
#     if not refresh_token:
#         raise HTTPException(status_code=404, detail="refresh_token不存在")

#     # 标记为已注销
#     upd = (
#         update(RefreshToken)
#         .where(RefreshToken.jti == refresh_jti)
#         .values(is_revoked=True)
#     )
#     await db.execute(upd)
#     await db.commit()

#     # 返回响应，前端收到后应删除本地 access_token
#     return LogoutResponse(message="注销成功，请删除本地 access_token")


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    # 检查 email/username 是否唯一
    result = await db.execute(select(User).where((User.email == req.email) | (User.username == req.username)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱或用户名已被注册")

    # 创建用户
    new_user = User(
        email=req.email,
        username=req.username,
        password_hash=get_password_hash(req.password),  # 密码哈希
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="注册失败，邮箱或用户名已存在")

    return UserRegisterResponse(id=new_user.id, created_at=new_user.created_at)


# 刷新 access token， 返回 access refresh token
@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_access_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db), request: Request = None):
    # 从某个地方获取 refresh token
    token_hash = get_password_hash(req.refresh_token)
    token_uuid = get_uuid(req.refresh_token)
    result = await db.execute(
        RefreshToken.__table__.select().where(
            RefreshToken.token_hash == token_hash,  # refresh hash 值存在
            RefreshToken.jti == token_uuid,
            RefreshToken.is_revoked == False,  # noqa: E712 不在黑名单里
            RefreshToken.expires_at > datetime.utcnow(),  # token 没过期
        )
    )
    token_row = result.fetchone()
    # refresh 过期, 需要警告，重新获取 refresh token
    if not token_row:
        raise HTTPException(status_code=401, detail="Refresh token invalid or expired")

    # 生成新的 access token
    access_token = create_access_token(token_row.user_id)

    # 返回 access token + refresh token
    return RefreshTokenResponse(access_token=access_token, refresh_token=req.refresh_token)


# 撤销 revoke_refresh （登出/黑名单）
@router.post("/revoke_refresh", response_model=RevokeRefreshTokenResponse)
async def revoke_refresh_token(req: RevokeRefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    token_uuid = get_uuid(req.refresh_token)
    result = await db.execute(
        RefreshToken.__table__
        .update()
        .where(RefreshToken.jti == token_uuid, RefreshToken.is_revoked == False)  # noqa: E712
        .values(is_revoked=True)
        .returning(RefreshToken.id)
    )
    token_row = result.fetchone()
    await db.commit()
    if not token_row:
        return RevokeRefreshTokenResponse(revoked=False, message="Token not found or already revoked")
    return RevokeRefreshTokenResponse(revoked=True, message="Token revoked successfully")
