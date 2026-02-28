from fastapi import FastAPI, HTTPException, Depends
from configparser import ConfigParser
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
import uvicorn

# 数据库URL
DATABASE_URL = ConfigParser().read('config/config.ini').get('postgresql', 'DATABASE_URL')

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True, future=True)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础类
Base = declarative_base()

# 定义用户模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/")
async def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def main():
    uvicorn.run(app="asyncio_sqlalchemy:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()