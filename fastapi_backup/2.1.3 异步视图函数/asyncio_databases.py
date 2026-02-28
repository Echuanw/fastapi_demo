from contextlib import asynccontextmanager
from configparser import ConfigParser
from fastapi import FastAPI, HTTPException
from databases import Database
import uvicorn
import asyncpg
import os


# 读取配置文件
config = ConfigParser()
config.read('config/config.ini')

# 从配置文件中获取数据库URL
DATABASE_URL = config.get('postgresql', 'DATABASE_URL')


# 创建数据库连接
database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect() 
    yield
    await database.disconnect()

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    user = await database.fetch_one(query=query, values={"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def main():
    uvicorn.run(app="asyncio_databases:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()