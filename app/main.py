from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()


# 创建FastAPI应用实例
app = FastAPI(
    title="用户管理系统",
    description="基于FastAPI、asyncio SQLAlchemy和PostgreSQL的用户管理系统",
    version="1.0.0"
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用用户管理系统",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}       # rediculous


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST"),
        port=int(os.getenv("APP_PORT")),
        reload=True
    )