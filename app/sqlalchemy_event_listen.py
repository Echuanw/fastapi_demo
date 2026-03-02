import asyncio
import logging
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
ASYNC_DATABASE_URL = config.get('postgresql', 'ASYNC_DATABASE_URL')

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建基类
Base = declarative_base()

# 定义模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# 创建异步数据库引擎
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

# 创建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# 定义事件处理函数
def before_insert_listener(mapper, connection, target):
    logger.info(f"About to insert User: {target.name}")
# 定义事件处理函数
def before_delete_listener(mapper, connection, target):
    logger.info(f"About to Delete User: {target.name}")

# 动态绑定事件
def bind_events(debug_mode):
    if debug_mode:
        event.listen(User, 'before_insert', before_insert_listener)
        event.listen(User, 'before_delete', before_delete_listener)
        logger.info("Event listener for 'before_insert', 'before_delete' is enabled.")
    else:
        logger.info("Event listener for 'before_insert', 'before_delete' is disabled.")

# 使用异步会话进行数据库操作
async def main(debug_mode):
    # 动态绑定事件
    bind_events(debug_mode)

    await create_tables()

    async with AsyncSessionLocal() as session:
        # 插入操作
        new_user = User(name='Alice')
        session.add(new_user)
        await session.commit()
        
        # 删除操作
        await session.delete(new_user)
        await session.commit()

if __name__ == "__main__":
    # 设置调试模式
    debug_mode = True  # 在调试模式下启用事件监听

    # ERROR : Event loop is closed  一个程序中多次调用asyncio.run, 会启用多个 event loop, 应该可以使用一个单独的事件循环来运行多个异步任务，而不是多次调用 asyncio.run()
    # asyncio.run(create_tables())      # 加到 main 里面了
    # asyncio.run(main(debug_mode))

    # 创建一个单独的 event loop
    asyncio.run(main(debug_mode))