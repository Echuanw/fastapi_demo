# create 01_fastapi.py 
from fastapi import FastAPI

# web 服务器
import uvicorn

# 框架本身，fastapi 对象，用于构建路由
app = FastAPI()

# 路由访问
    # 根页面 /
    # 指定页面 /xxx
    
@app.get("/")
async def root():
    return {"message": "Hello Fastapi Applications!"}
    
@app.get("/page1")
async def root():
    return {"message": "welcome page1!"}
    
@app.get("/page/page2")
async def root():
    return {"message": "welcome page2!"}

def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="01_fastapi:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()