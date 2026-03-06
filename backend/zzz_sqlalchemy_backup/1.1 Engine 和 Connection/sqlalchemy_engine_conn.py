from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()

# 从配置文件中获取数据库URL
DATABASE_URL = os.getenv('DATABASE_URL')

# 创建引擎时配置连接池
engine = create_engine(
    DATABASE_URL,
    pool_size=5,         # 连接池中连接的最大数量
    max_overflow=10,      # 允许溢出的连接数量
    pool_timeout=30,      # 获取连接的超时时间（秒）
    pool_recycle=1800     # 连接的回收时间（秒）
)

# 使用引擎进行数据库操作
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)