import asyncio
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select, insert, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()

# 从配置文件中获取数据库URL
ASYNC_DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')

# 创建基类
Base = declarative_base()

# 定义Account模型类
class Account(Base):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'cn'}  # 指定Schema

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 是否打印SQL语句日志
    future=True
)

# 创建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def async_crud_operations():
    # 异步 Session 上下文管理
    async with AsyncSessionLocal() as session:
        # 使用原生SQL语句进行TRUNCATE
        await session.execute(text("TRUNCATE TABLE cn.accounts CASCADE"))
        await session.commit()

        # 1. select 查询全部
        print("1 Initial data:")
        stmt = select(Account)
        result = await session.execute(stmt)
        for row in result.scalars():
            print(f"ID: {row.id}, Username: {row.username}, Email: {row.email}, Created At: {row.created_at}, Is Active: {row.is_active}")

        # 2. Insert 插入几条数据
        # 2.1 插入1条
        await session.execute(insert(Account).values(username='new_user', email='new_user@example.com'))
        # 2.2 批量插入
        await session.execute(insert(Account), [
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
            {"username": "charlie", "email": "charlie@example.com"}
        ])
        await session.commit()

        # 3. select 查询全部
        print("\n3 After insert:")
        stmt = select(Account)
        result = await session.execute(stmt)
        for row in result.scalars():
            print(f"ID: {row.id}, Username: {row.username}, Email: {row.email}, Created At: {row.created_at}, Is Active: {row.is_active}")

        # 4. update 几条数据
        await session.execute(update(Account).where(Account.username == "alice").values(email="alice_new@example.com"))
        await session.execute(update(Account).where(Account.username == "bob").values(is_active=False))
        await session.commit()

        # 5. select 查询全部
        print("\nAfter update:")
        stmt = select(Account)
        result = await session.execute(stmt)
        for row in result.scalars():
            print(f"ID: {row.id}, Username: {row.username}, Email: {row.email}, Created At: {row.created_at}, Is Active: {row.is_active}")

        # 6. delete 几条数据
        await session.execute(delete(Account).where(Account.username == "charlie"))
        await session.commit()

        # 7. select 查询全部
        print("\nAfter delete:")
        stmt = select(Account)
        result = await session.execute(stmt)
        for row in result.scalars():
            print(f"ID: {row.id}, Username: {row.username}, Email: {row.email}, Created At: {row.created_at}, Is Active: {row.is_active}")

        # 8. upsert
        accounts_to_upsert = [
            {"username": "alice", "email": "alice_new@example.com"},
            {"username": "bob", "email": "bob_new@example.com"},
            {"username": "charlie", "email": "charlie@example.com"}
        ]

        for account_data in accounts_to_upsert:
            account = await session.execute(select(Account).filter_by(username=account_data['username']))
            account_instance = account.scalars().first()
            if account_instance:
                account_instance.email = account_data['email']
            else:
                account_instance = Account(**account_data)
                session.add(account_instance)
        await session.commit()

        # 9. select 查询全部
        print("\nAfter upsert:")
        stmt = select(Account)
        result = await session.execute(stmt)
        for row in result.scalars():
            print(f"ID: {row.id}, Username: {row.username}, Email: {row.email}, Created At: {row.created_at}, Is Active: {row.is_active}")

# 运行异步操作
async def main():
    await create_tables()
    await async_crud_operations()

asyncio.run(main())