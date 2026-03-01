from sqlalchemy import create_engine, Column, Integer, BigInteger, Numeric, Boolean, String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
DATABASE_URL = config.get('postgresql', 'DATABASE_URL')

# 创建基类
Base = declarative_base()

# 定义第一个ORM模型类
class Account(Base):
    __tablename__ = 'accounts'  # 表名
    __table_args__ = {'schema': 'cn'}  # 指定Schema

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    # 关系定义， Profile 是类名，account 是 Profile 类中定义的关系
    profiles = relationship("Profile", back_populates="account")

# 定义第二个ORM模型类
class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'cn'}  # 指定Schema

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('cn.accounts.id'), nullable=False)  # 更改外键引用
    bio = Column(Text)
    age = Column(Integer)
    balance = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.now)

    # 关系定义
    account = relationship("Account", back_populates="profiles")

# 创建引擎（示例使用SQLite）
engine = create_engine(DATABASE_URL, echo=True)

# 创建表
Base.metadata.create_all(engine)