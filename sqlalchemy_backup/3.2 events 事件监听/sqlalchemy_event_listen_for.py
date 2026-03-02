import logging
from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import sessionmaker, declarative_base
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
DATABASE_URL = config.get('postgresql', 'DATABASE_URL')


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

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=False)

# 创建表
Base.metadata.create_all(engine)

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)

# 定义事件处理函数，定义好操作函数 和 监听事件后，会自动在事件发生时触发并调用
@event.listens_for(User, 'before_insert')
def before_insert_listener(mapper, connection, target):
    logger.info(f"About to insert User: {target.name}")

@event.listens_for(User, 'after_insert')
def before_insert_listener(mapper, connection, target):
    logger.info(f"insert User: {target.name} SUCCESS")

@event.listens_for(User, 'before_update')
def before_update_listener(mapper, connection, target):
    logger.info(f"About to update User: {target.name}")

@event.listens_for(User, 'after_update')
def before_insert_listener(mapper, connection, target):
    logger.info(f"update User: {target.name} SUCCESS")

@event.listens_for(User, 'before_delete')
def before_delete_listener(mapper, connection, target):
    logger.info(f"About to delete User: {target.name}")

@event.listens_for(User, 'after_delete')
def before_insert_listener(mapper, connection, target):
    logger.info(f"delete User: {target.name} SUCCESS")

# 使用会话进行数据库操作
def main():
    session = SessionLocal()

    # 插入操作
    new_user = User(name='Alice')
    session.add(new_user)
    session.commit()

    # 更新操作
    new_user.name = 'Alice Updated'
    session.commit()

    # 删除操作
    session.delete(new_user)
    session.commit()

if __name__ == "__main__":
    main()