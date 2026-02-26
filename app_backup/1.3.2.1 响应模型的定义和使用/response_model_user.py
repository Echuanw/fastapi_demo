import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# 模拟密码加密上下文
def get_password_hash(password: str) -> str:
    return "encrypt_" + password

# 响应模型的定义 - 输入模型
class UserInput(BaseModel):
    username: str
    password: str
# 响应模型的定义 - 输出模型
class UserOutput(BaseModel):
    username: str
# 响应模型的定义 - 数据库模型
class UserInDB(BaseModel):
    username: str
    hashed_password: str

# 模拟数据库
fake_db: List[UserInDB] = []

# POST端点用于创建新用户，并返回不含密码的用户信息。
@app.post("/users/", response_model=UserOutput)
def create_user(user: UserInput):
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed_password)
    print("user_in_db : " + str(user_in_db))    # output user in db
    fake_db.append(user_in_db)
    return UserOutput(username=user.username)

# GET端点用于获取所有用户信息，不包含密码。
@app.get("/users/", response_model=List[UserOutput])
def read_users():
    return [UserOutput(username=user.username) for user in fake_db]

def main():
    uvicorn.run(app="response_model_user:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()