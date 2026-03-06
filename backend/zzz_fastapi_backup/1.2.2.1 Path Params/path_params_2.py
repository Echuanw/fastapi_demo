from fastapi import FastAPI
import uvicorn
# Path Params Enum预设值
from enum import Enum

# 1 创建枚举的预设值
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "hello fastapi user"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # 比较枚举对象
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}    # 输入 /models/alexnet
	# 比较枚举对象的值
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}  # 输入 /models/lenet
    return {"model_name": model_name, "message": "Have some residuals"}       # 输入 /models/resnet

def main():
    """
    app 启动的py文件名
    host port 访问的ip端口
    reload .,.
    """
    uvicorn.run(app="path_params_2:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()