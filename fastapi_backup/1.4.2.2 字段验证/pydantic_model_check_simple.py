import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义 Pydantic 模型
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

    # 如果客户端发送的 JSON 包含其他字段，FastAPI 会返回一个 422 错误
    class Config:
        extra = 'forbid'  # 使用字符串字面值代替 Extra.forbid

# 使用模型进行数据验证和解析
@app.post("/items/")
async def create_item(item: Item):
    return item

def main():
    uvicorn.run(app="pydantic_model_check_simple:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()