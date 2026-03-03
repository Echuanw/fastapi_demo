from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()

# 从配置文件中获取数据库URL
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

# 定义ORM模型
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# 创建表，表存在不会对现有表产生影响
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def main():
    # session = Session()            # 【会话管理】使用 with 替代了
    with Session() as session:
        try:
            # 【对象持久化】：添加新用户
            new_user = User(name='David', email='david@example.com')
            session.add(new_user)
            session.commit()  # 【事务管理】提交事务
            new_user = User(name='Test', email='test@example.com')
            session.add(new_user)
            session.commit()  # 【事务管理】提交事务

            # 【数据查询】：查询所有用户
            users = session.query(User).all()
            for user in users:
                print(f"User {user.id}: {user.name}, {user.email}")

            # 【对象持久化】：删除用户
            user_to_delete = session.query(User).filter_by(name='David').first()
            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()  # 【事务管理】提交事务

        except Exception as e:
            session.rollback()  # 【事务管理】回滚事务
            print(f"An error occurred: {e}")

    # finally:
    #     session.close()        # 【会话管理】确保Session在使用后被正确关闭，被 with 替代了

if __name__ == "__main__":
    main()