from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.crud.user import UserCRUD
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新用户"""
    user_crud = UserCRUD(db)
    
    # 检查用户名是否已存在
    existing_user = await user_crud.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = await user_crud.get_user_by_email(user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="邮箱已存在"
        )
    
    user = await user_crud.create_user(user_create)
    return user


@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db)
):
    """获取用户列表"""
    user_crud = UserCRUD(db)
    skip = (page - 1) * size
    
    users, total = await user_crud.get_users(
        skip=skip, 
        limit=size, 
        is_active=is_active
    )
    
    return UserListResponse(
        users=users,
        total=total,
        page=page,
        size=size
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """根据ID获取用户"""
    user_crud = UserCRUD(db)
    user = await user_crud.get_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    user_crud = UserCRUD(db)
    
    # 检查用户是否存在
    existing_user = await user_crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    # 如果更新用户名，检查是否已存在
    if user_update.username and user_update.username != existing_user.username:
        username_exists = await user_crud.get_user_by_username(user_update.username)
        if username_exists:
            raise HTTPException(
                status_code=400,
                detail="用户名已存在"
            )
    
    # 如果更新邮箱，检查是否已存在
    if user_update.email and user_update.email != existing_user.email:
        email_exists = await user_crud.get_user_by_email(user_update.email)
        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="邮箱已存在"
            )
    
    user = await user_crud.update_user(user_id, user_update)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除用户"""
    user_crud = UserCRUD(db)
    
    success = await user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """根据用户名获取用户"""
    user_crud = UserCRUD(db)
    user = await user_crud.get_user_by_username(username)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    return user


@router.post("/authenticate")
async def authenticate_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """用户认证"""
    user_crud = UserCRUD(db)
    user = await user_crud.authenticate_user(username, password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )
    
    return {
        "message": "认证成功",
        "user": user
    }