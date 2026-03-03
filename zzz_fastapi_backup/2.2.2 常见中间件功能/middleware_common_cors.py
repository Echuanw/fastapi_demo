from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# 定义允许的源
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://example.com",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],    # 允许的 HTTP 方法
    allow_headers=["*"],    # 允许的 HTTP 头
)

@app.get("/")
async def read_main():
    return {"message": "Hello World"}

def main():
    uvicorn.run(app="middleware_common_log:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()