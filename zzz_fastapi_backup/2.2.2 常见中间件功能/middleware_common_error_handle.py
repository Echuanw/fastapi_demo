# 通过中间件实现统一的错误处理。这样可以捕获应用中的异常，并以一致的方式进行处理和响应。
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

app = FastAPI()

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # 在这里可以记录日志或执行其他错误处理逻辑
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error", "details": str(exc)},
            )

# 将中间件添加到应用中
app.add_middleware(ExceptionHandlingMiddleware)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/error")
async def create_error():
    raise ValueError("This is an intentional error")

def main():
    uvicorn.run(app="middleware_common_error_handle:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()