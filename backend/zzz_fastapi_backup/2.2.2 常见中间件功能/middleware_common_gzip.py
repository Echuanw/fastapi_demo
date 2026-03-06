from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

app = FastAPI()

# 添加 GZip 中间件
# minimum_size 参数指定了响应体的最小字节数，只有大于这个大小的响应才会被压缩。
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# 其他路由和逻辑
def main():
    uvicorn.run(app="middleware_common_log:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()