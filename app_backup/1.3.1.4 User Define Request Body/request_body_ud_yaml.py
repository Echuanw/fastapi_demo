import uvicorn

# 在 FastAPI 中处理 YAML 格式的请求体。
from fastapi import FastAPI, Request, HTTPException
import yaml

app = FastAPI()

@app.post("/yaml/")
async def read_yaml(request: Request):
    try:
        # 读取请求体中的原始数据
        body = await request.body()
        # 将 YAML 数据解析为 Python 字典
        data = yaml.safe_load(body)
        return {"parsed_data": data}
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail="Invalid YAML format")

def main():
    uvicorn.run(app="request_body_ud_yaml:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()