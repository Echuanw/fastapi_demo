import uvicorn

from fastapi import FastAPI, status
app = FastAPI()

# status. 下有多种响应状态码
#	- 200 是默认响应码，表示一切正常
#	- 201 表示已创建，通常在数据库中创建新记录后使用
#	- 204 是一种特殊的例子，表示无内容。该响应在没有返回内容时使用，因此，不能包含响应体
#	- 404，用于未找到响应。

@app.post("/items/", status_code=status.HTTP_201_CREATED)     # 等同于 status_code=201
async def create_item(name: str):
    return {"name": name}

def main():
    uvicorn.run(app="response_status_code:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()