# 简单的中间件示例，它记录每个请求的处理时间
import asyncio

from fastapi import FastAPI
import time
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

app = FastAPI()

# 定义中间件
# 创建了一个 SimpleMiddleware 类，继承自 BaseHTTPMiddleware。
# dispatch 方法，记录了请求的开始时间和结束时间，并将处理时间添加到响应头中。
class SimpleMiddleware1(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        await asyncio.sleep(1)
        response = await call_next(request)
        await asyncio.sleep(1)
        end_time = time.time()
        process_time = end_time - start_time
        print(f"SimpleMiddleware1 start at {start_time}, end at {end_time}, process time is {process_time}")
        response.headers["X-Process-Time1"] = str(process_time)
        return response
        
        
class SimpleMiddleware2(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        await asyncio.sleep(1)
        response = await call_next(request)
        await asyncio.sleep(1)
        end_time = time.time()
        process_time = end_time - start_time
        print(f"SimpleMiddleware2 start at {start_time}, end at {end_time}, process time is {process_time}")
        response.headers["X-Process-Time2"] = str(process_time)
        return response

# 添加中间件到应用
# 中间件全局范围生效，会处理所有请求和响应。
# 不能为特定的路径操作或路由单独设置。
app.add_middleware(SimpleMiddleware1)
app.add_middleware(SimpleMiddleware2)

@app.get("/")
async def read_main():
    return {"message": "Hello World"}

def main():
    uvicorn.run(app="middleware_record_time:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()