from fastapi import FastAPI

# web 服务器
import uvicorn

# 框架本身，fastapi 对象，用于构建路由
app = FastAPI()

# 增删改查
    # @app.put()
    # @app.delete()
    # @app.post()
    # @app.get()
# 自动生成API文档
    # /docs

# Fastapi 中使用 `@app.get()`、`@app.post()`、`@app.put()`、`@app.delete()` 等装饰器来定义路由

@app.get('/')
async def root():
    return {"message": "hello fastapi user"}

@app.put('/put')
async def put_test():
    return {"method":"put() 方法"}
     
@app.delete('/delete')
async def delete_test():
    return {"method":"delete() 方法"}
     
@app.post('/post')
async def post_test():
    return {"method":"post() 方法"}
     
@app.get('/get')
async def get_test():
    return {"method":"get() 方法"}


def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()