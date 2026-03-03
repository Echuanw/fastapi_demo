from fastapi import FastAPI
from pydantic import BaseModel     # pydantic 属于数据模型和数据校验部分的内容
import uvicorn

# 假设我们有一个用户注册的场景，客户端需要向服务器发送用户的注册信息，包括用户名、邮箱和密码。
# 客户端会以 JSON 格式发送这些数据。
app = FastAPI()

class User(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
async def register_user(user: User):
    # 这里可以处理注册逻辑，比如保存到数据库
    return {"message": f"User {user.username} registered successfully"}


def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="request_body_json:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()