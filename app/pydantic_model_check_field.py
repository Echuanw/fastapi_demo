import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

# 定义 Pydantic 模型
class Product(BaseModel):
    name: str = Field(..., min_length=5, description="商品名称，必须提供，至少5个字符")
    price: float = Field(..., gt=0, description="商品价格，必须为正数")
    stock: int = Field(100, ge=0, description="库存数量，默认值100，必须为非负整数")
    desc: str = Field(None, max_length=200, description="商品描述，可以为空，最大200字符")

    # 自定义验证器
    @field_validator('name')
    def name_must_contain_space(cls, v):
        if not(str(v).startswith( "SKU" )):
            raise ValueError('name must start with SKU')
        return v

# 使用模型进行数据验证和解析
@app.post("/products/")
async def create_product(product: Product):
    # 模拟数据库操作
    if product.name == "Existing Product":
        raise HTTPException(status_code=400, detail="Product already exists")
    return {"message": "Product created successfully", "product": product}
def main():
    uvicorn.run(app="pydantic_model_check_field:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()