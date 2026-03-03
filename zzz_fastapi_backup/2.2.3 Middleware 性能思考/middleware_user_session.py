import asyncpg
from redis.asyncio import Redis
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
from dotenv import load_dotenv
import os

import uvicorn

# 注册环境变量
load_dotenv()

# 从配置文件中获取数据库URL
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_URL = os.getenv('REDIS_URL')

app = FastAPI()

async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

async def get_redis():
    return await Redis.from_url(
            REDIS_URL,
            password=REDIS_PASSWORD,
            decode_responses=True,  # 返回字符串而不是字节
        )

# 从数据库中获取用户信息
async def fetch_user_from_db(pool, username: str) -> Dict:
    async with pool.acquire() as connection:
        result = await connection.fetchrow("SELECT username, permissions FROM users WHERE username = $1", username)
        if result:
            return dict(result)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

# 中间件来处理用户会话缓存
@app.middleware("http")
async def user_session_middleware(request: Request, call_next):
    username = request.headers.get("X-Username")
    if not username:
        return JSONResponse(status_code=400, content={"detail": "Username header missing"})
    redis = await get_redis()
    user_session = await redis.get(username)
    if not user_session:
        # 如果缓存中没有用户数据，从数据库中获取
        db_pool = await get_db_pool()
        try:
            print("Cache miss - Fetched from DB")
            user_session = await fetch_user_from_db(db_pool, username)
            # 将用户数据存储到Redis缓存中
            await redis.set(username, str(user_session), ex=60)  # 设置缓存过期时间为1小时
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    request.state.user = user_session  # 将字符串转换为字典
    response = await call_next(request)
    return response

@app.get("/items/")
async def read_items(request: Request):
    user = request.state.user
    return {"message": f"Hello {user}"}

def main():
    uvicorn.run(app="middleware_user_session:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()