from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import argon2
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.database import get_db
from backend.models import User
from backend.schemas import UserRegisterRequest, UserRegisterResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    req: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    # 检查 email/username 是否唯一
    result = await db.execute(
        select(User).where((User.email == req.email) | (User.username == req.username))
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱或用户名已被注册"
        )

    # 密码哈希
    password_hash = argon2.hash(req.password)

    # 创建用户
    new_user = User(
        email=req.email,
        username=req.username,
        password_hash=password_hash
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="注册失败，邮箱或用户名已存在"
        )

    return UserRegisterResponse(
        id=new_user.id,
        created_at=new_user.created_at
    )
