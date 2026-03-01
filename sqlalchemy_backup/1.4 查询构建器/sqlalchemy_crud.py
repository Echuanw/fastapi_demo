from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, select, insert, text, update, delete
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
DATABASE_URL = config.get('postgresql', 'DATABASE_URL')
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

# 创建引擎（示例使用SQLite）
engine = create_engine(DATABASE_URL, echo=False)

# 创建表
Base.metadata.create_all(engine)

# 使用Session进行数据库操作
with Session(engine) as session:
    # 使用原生SQL语句进行TRUNCATE
    session.execute(text("TRUNCATE TABLE cn.accounts CASCADE"))
    session.commit()


    # 1. select 查询全部
    print("1 Initial data:")
    stmt = select(Account)
    result = session.execute(stmt)
    for row in result:
        print(f"ID: {row[0].id}, Username: {row[0].username}, Email: {row[0].email}, Created At: {row[0].created_at}, Is Active: {row[0].is_active}")

    # 2. Insert 插入几条数据
    # 2.1 插入1条
    session.execute(insert(Account).values(username='new_user', email='new_user@example.com'))
    # 2.2 批量插入
    session.execute(insert(Account), [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"},
        {"username": "charlie", "email": "charlie@example.com"}
    ])
    session.commit()

    # 3. select 查询全部
    print("\n3 After insert:")
    stmt = select(Account)
    result = session.execute(stmt)
    for row in result:
        print(f"ID: {row[0].id}, Username: {row[0].username}, Email: {row[0].email}, Created At: {row[0].created_at}, Is Active: {row[0].is_active}")

    # 4. update 几条数据
    session.execute(update(Account).where(Account.username == "alice").values(email="alice_new@example.com"))
    session.execute(update(Account).where(Account.username == "bob").values(is_active=False))
    session.commit()

    # 5. select 查询全部
    print("\nAfter update:")
    stmt = select(Account)
    result = session.execute(stmt)
    for row in result:
        print(f"ID: {row[0].id}, Username: {row[0].username}, Email: {row[0].email}, Created At: {row[0].created_at}, Is Active: {row[0].is_active}")

    # 6. delete 几条数据
    session.execute(delete(Account).where(Account.username == "charlie"))
    session.commit()

    # 7. select 查询全部
    print("\nAfter delete:")
    stmt = select(Account)
    result = session.execute(stmt)
    for row in result:
        print(f"ID: {row[0].id}, Username: {row[0].username}, Email: {row[0].email}, Created At: {row[0].created_at}, Is Active: {row[0].is_active}")

    # 8. upsert 
    # 数据库特性：不同数据库支持不同的upsert语法，使用SQLAlchemy时可以利用这些特性。
    # 手动实现：在不支持upsert的数据库中，可以通过查询和条件逻辑手动实现。

    # 要进行upsert的账户数据
    accounts_to_upsert = [
        {"username": "alice", "email": "alice_new@example.com"},
        {"username": "bob", "email": "bob_new@example.com"},
        {"username": "charlie", "email": "charlie@example.com"}
    ]

    for account_data in accounts_to_upsert:
        # 查询是否存在
        account = session.query(Account).filter_by(username=account_data['username']).first()
        if account:
            # 更新
            account.email = account_data['email']
        else:
            # 插入
            account = Account(**account_data)
            session.add(account)
    session.commit()

    # 9. select 查询全部
    print("\nAfter upsert:")    
    stmt = select(Account)
    result = session.execute(stmt)
    for row in result:
        print(f"ID: {row[0].id}, Username: {row[0].username}, Email: {row[0].email}, Created At: {row[0].created_at}, Is Active: {row[0].is_active}")




