from fastapi import FastAPI, Request
import logging
import time

import uvicorn

# 创建 FastAPI 应用
app = FastAPI()

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 记录请求信息
    logger.info(f"Request: {request.method} {request.url}")
    # 记录请求开始时间
    start_time = time.time()
    # 调用下一个中间件或实际的请求处理函数
    response = await call_next(request)
    # 计算请求处理时间
    process_time = time.time() - start_time
    # 记录响应信息
    logger.info(f"Response: {response.status_code} (Processed in {process_time:.2f} seconds)")
    return response

# 示例路由
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

def main():
    uvicorn.run(app="middleware_common_log:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()