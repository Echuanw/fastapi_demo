import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# 定义嵌套的子模型
class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class Company(BaseModel):
    name: str
    founded: int
    employees: int

# 定义主模型
class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None
    addresses: List[Address] = []
    company: Optional[Company] = None

app = FastAPI()

fakedb: List[User] = []

@app.post("/users/")
async def create_user(user: User):
    fakedb.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def get_users():
    return fakedb

def main():
    uvicorn.run(app="pydantic_nested_model:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()