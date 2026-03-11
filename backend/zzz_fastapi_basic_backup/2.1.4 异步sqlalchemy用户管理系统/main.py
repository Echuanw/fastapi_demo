from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# 注册环境变量
load_dotenv()

from app.core.database import create_tables, drop_tables
from app.api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建数据库表
    # await drop_tables()        # 测试
    await create_tables()
    print("数据库表创建完成")
    yield
    # 关闭时的清理工作
    print("应用关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title="用户管理系统",
    description="基于FastAPI、asyncio SQLAlchemy和PostgreSQL的用户管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# 注册路由
app.include_router(users_router, prefix="/api/v1")


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