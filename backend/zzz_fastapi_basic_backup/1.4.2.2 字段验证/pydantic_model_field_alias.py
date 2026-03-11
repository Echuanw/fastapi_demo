import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class PaymentRequest(BaseModel):
    user_id: int = Field(..., alias='userId')
    transaction_amount: float = Field(..., alias='transactionAmount')
    payment_method: str = Field(..., alias='paymentMethod')

@app.post("/process-payment/")
async def process_payment(payment_request: PaymentRequest):
    # 在这里处理支付请求，接受的参数是驼峰格式
    # 但是处理的时候，就可以直接使用下划线 payment_request.user_id ......
    return {"message": "Payment processed successfully", "data": payment_request}

def main():
    uvicorn.run(app="pydantic_model_field_alias:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()