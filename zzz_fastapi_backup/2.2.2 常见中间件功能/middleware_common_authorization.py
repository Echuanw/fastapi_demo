from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 从请求头中获取认证信息
        auth_header = request.headers.get('Authorization')
        
        # 简单的认证逻辑：检查认证信息是否存在且符合预期
        if auth_header != "Bearer mysecrettoken":
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # 继续处理请求
        response = await call_next(request)
        return response

# 将中间件添加到FastAPI应用
app.add_middleware(AuthMiddleware)

@app.get("/protected")
async def protected_route():
    return {"message": "This is a protected route"}

@app.get("/open")
async def open_route():
    return {"message": "This is an open route"}

def main():
    uvicorn.run(app="middleware_common_authorization:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()