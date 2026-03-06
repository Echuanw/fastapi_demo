from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from passlib.hash import argon2

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return argon2.verify(plain_password, hashed_password)    # 密码 与 hash 值进行校验


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return argon2.hash(password)                             # 密码 hash


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """获取用户列表"""
        query = select(User)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        # 获取总数
        count_query = select(func.count(User.id))
        if is_active is not None:
            count_query = count_query.where(User.is_active == is_active)
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return list(users), total

    async def create_user(self, user_create: UserCreate) -> User:
        """创建用户"""
        hashed_password = get_password_hash(user_create.password)
        
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=user_create.is_active,
            is_superuser=user_create.is_superuser,
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = await self.get_user(user_id)
        if not db_user:
            return None
        
        # 新数据的对象转成 dict格式，并且将没设置的kv删除（在这删除了默认值）
        update_data = user_update.model_dump(exclude_unset=True)     
        
        # 如果更新密码，需要加密
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():     # 更新
            setattr(db_user, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        db_user = await self.get_user(user_id)
        if not db_user:
            return False
        
        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user