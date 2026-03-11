# 用户管理系统

基于 FastAPI、asyncio SQLAlchemy 和 PostgreSQL 的简单用户管理系统。

## 功能特性

- ✅ 用户创建、查询、更新、删除 (CRUD)
- ✅ 异步数据库操作
- ✅ 密码加密存储
- ✅ 数据验证和序列化
- ✅ RESTful API 设计
- ✅ 自动生成 API 文档
- ✅ 分页查询支持
- ✅ 用户认证功能

## 项目结构

```
app/
├── __init__.py
├── main.py                 # FastAPI 应用入口
├── requirements.txt        # 项目依赖
├── README.md              # 项目说明
├── api/                   # API 路由
│   ├── __init__.py
│   └── users.py           # 用户相关路由
├── core/                  # 核心配置
│   ├── __init__.py
│   └── database.py        # 数据库配置
├── crud/                  # 数据库操作
│   ├── __init__.py
│   └── user.py            # 用户 CRUD 操作
├── models/                # 数据库模型
│   ├── __init__.py
│   └── user.py            # 用户模型
└── schemas/               # Pydantic 模型
    ├── __init__.py
    └── user.py            # 用户数据模型
```

## 环境要求

- Python 3.8+
- PostgreSQL 12+

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

创建 PostgreSQL 数据库，并设置环境变量：

```bash
export DATABASE_URL="postgresql+asyncpg://username:password@localhost/user_management"
```

或者在代码中直接修改 `app/core/database.py` 中的数据库连接字符串。

### 3. 运行应用

```bash
# 方式1：直接运行
python -m app.main

# 方式2：使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问应用

- 应用地址: http://localhost:8000
- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

## API 接口

### 用户管理

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/users/` | 创建用户 |
| GET | `/api/v1/users/` | 获取用户列表 |
| GET | `/api/v1/users/{user_id}` | 获取指定用户 |
| PUT | `/api/v1/users/{user_id}` | 更新用户信息 |
| DELETE | `/api/v1/users/{user_id}` | 删除用户 |
| GET | `/api/v1/users/username/{username}` | 根据用户名获取用户 |
| POST | `/api/v1/users/authenticate` | 用户认证 |

### 示例请求

#### 创建用户

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "full_name": "Test User",
       "password": "password123",
       "is_active": true,
       "is_superuser": false
     }'
```

#### 获取用户列表

```bash
curl "http://localhost:8000/api/v1/users/?page=1&size=10"
```

#### 用户认证

```bash
curl -X POST "http://localhost:8000/api/v1/users/authenticate" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=password123"
```

## 数据模型

### User 模型

```python
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

## 开发说明

### 数据库迁移

应用启动时会自动创建数据库表。如果需要手动管理，可以使用：

```python
from app.core.database import create_tables, drop_tables

# 创建表
await create_tables()

# 删除表
await drop_tables()
```

### 密码安全

- 使用 bcrypt 算法加密密码
- 密码不会在 API 响应中返回
- 支持密码验证功能

### 异步支持

- 所有数据库操作都是异步的
- 使用 asyncpg 作为 PostgreSQL 异步驱动
- 支持高并发请求处理

## 许可证

MIT License