import asyncio
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select, insert, update, delete, text, func
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
        pass
        # # 使用原生SQL语句进行TRUNCATE
        # await session.execute(text("TRUNCATE TABLE cn.accounts CASCADE"))
        # await session.commit()

        # # 1. 别名
        # print("1 别名:")
        # stmt = select(func.count(Account.id).label('user_count'))      # 字段别名


        # # 2. JOIN
        # # INNER JOIN
        # stmt = select(User, Order).join(Order, User.id == Order.user_id)

        # # LEFT JOIN
        # stmt = select(User, Order).outerjoin(Order, User.id == Order.user_id)

        # # 3. Where 条件
        # from sqlalchemy import select, and_, or_

        # # AND 条件
        # stmt = select(User).where(and_(User.name == 'Alice', User.age > 30))

        # # OR 条件
        # stmt = select(User).where(or_(User.name == 'Alice', User.name == 'Bob'))


        # # 4. 子查询
        # # 创建子查询
        # subquery = select(Order.user_id, func.sum(Order.amount).label('total_amount')).group_by(Order.user_id).subquery()
        # # 使用子查询
        # stmt = select(User.name, subquery.c.total_amount).join(subquery, User.id == subquery.c.user_id)


        # # 5. CTE
        # # 第一个 CTE: 计算每个用户的订单总金额
        # order_total_cte = (
        #     select(Order.user_id, func.sum(Order.amount).label('total_amount'))
        #     .group_by(Order.user_id)
        #     .cte('order_total_cte')
        # )

        # # 第二个 CTE: 筛选出订单总金额超过 100 的用户
        # filtered_users_cte = (
        #     select(order_total_cte.c.user_id)
        #     .where(order_total_cte.c.total_amount > 100)
        #     .cte('filtered_users_cte')
        # )

        # # 使用多级 CTE 进行最终查询
        # stmt = (
        #     select(User.name, order_total_cte.c.total_amount)
        #     .join(filtered_users_cte, User.id == filtered_users_cte.c.user_id)
        #     .join(order_total_cte, User.id == order_total_cte.c.user_id)
        # )


# 运行异步操作
async def main():
    await create_tables()
    await async_crud_operations()

asyncio.run(main())