from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "hello fastapi user"}

@app.get("/users/me")               # 放在后面会把 me 识别成参数
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")        # 声明时用{}
async def read_user(user_id: str):  # 默认 str 类型，可以用其他类型
    return {"user_id": user_id}

# @app.get("/users/me")               # 放在后面会把 me 识别成参数
# async def read_user_me():
#     return {"user_id": "the current user"}


def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="path_params_1:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()