import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, select
from redis.asyncio import Redis
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()

# 从配置文件中获取数据库URL
ASYNC_DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_URL = os.getenv('REDIS_URL')

# 创建基类（SQLAlchemy 2.0 推荐导入路径）
Base = declarative_base()

# 定义User模型类
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# 创建异步引擎
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# 建议：全局复用 Redis 连接，避免每次函数都创建
redis_client: Redis | None = None

async def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = Redis.from_url(
            REDIS_URL,
            password=REDIS_PASSWORD,
            decode_responses=True,  # 返回字符串而不是字节
        )
    return redis_client

# 异步获取用户信息并缓存
async def get_user_info(user_id: int):
    redis = await get_redis()

    # 1. 先查缓存
    key = f"user:{user_id}"
    cached_user = await redis.get(key)
    if cached_user:
        print("Cache hit")
        return cached_user

    # 2. 未命中则查数据库
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            # 回写缓存，设置过期时间 60 秒
            await redis.set(key, user.name, ex=60)
            print("Cache miss - Fetched from DB")
            return user.name
        return None

async def main():
    # 第一次应为 miss，第二次应为 hit
    user_info = await get_user_info(1)
    print(f"User Info: {user_info}")

    user_info = await get_user_info(1)
    print(f"User Info: {user_info}")

    # 程序结束前可按需关闭 Redis 连接
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        await redis_client.connection_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())