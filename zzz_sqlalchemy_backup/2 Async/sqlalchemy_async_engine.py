import asyncio

from sqlalchemy import Column, Integer, String, DateTime, Boolean, text
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
    future=True,  # 使用SQLAlchemy 2.0的未来模式
    pool_size=5,  # 连接池的大小
    max_overflow=10,  # 连接池溢出时可以创建的最大连接数
    pool_timeout=30,  # 连接池获取连接的超时时间
    pool_recycle=1800,  # 连接池中连接的回收时间
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def query_accounts():
    # 使用异步上下文管理会话
    async with AsyncSessionLocal() as session:
        # 执行查询
        result = await session.execute(text("SELECT * FROM cn.accounts"))
        
        # 打印查询结果
        for row in result:     # return 
            print(row)

# 运行异步查询
asyncio.run(query_accounts())
