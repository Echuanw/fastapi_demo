from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "hello fastapi user"}

"""
user_id、item_id  路径参数
limit             自动识别为查询参数，且有默认值10
q                 自动识别为查询参数，默认值为None，是可选的。可加可不加
must_choose       自动识别为查询参数，没有默认值，所以是必须选的
"""
@app.get("/users/{user_id}/items/{item_id}")
async def read_item(user_id: str, item_id: str, must_choose: str, limit: int = 10, q: str | None = None):
    if q:
        return {"user_id": user_id, "item_id": item_id, "limit": limit, "q": q, "must_choose": must_choose}
    return {"user_id": user_id, "item_id": item_id, "limit": limit, "must_choose": must_choose}


def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="path_params_1:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()