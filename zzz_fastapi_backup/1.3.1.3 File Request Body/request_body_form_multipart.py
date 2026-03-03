import uvicorn

from typing import Optional
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# response_class=HTMLResponse 指定路由返回的是HTML内容。FastAPI会将返回的字符串作为HTML处理，并设置 Content-Type为text/html
@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Upload File</title>
        </head>
        <body>
            <h1>Upload File</h1>
            
            <p> 
            对于复杂内容的表单，enctype="multipart/form-data"是必须的 <br>
            接受一个 text 类型的，赋值给 username <br>
            接受一个 file 类型的，赋值给 file <br>
            点击 submit后，使用POST方法提交数据到/upload/路径
            </p>

            <form action="/upload/" method="post" enctype="multipart/form-data">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="file">File:</label>
                <input type="file" id="file" name="file"><br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

@app.post("/upload/")
# username: str = Form(...)：表示username是一个必需的表单字段，必须在请求中提供。
# file: UploadFile = File(...)：表示file是一个必需的文件字段，必须在请求中提供。
# UploadFile 官方文档 : https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
async def upload_file(username: str = Form(...), file: UploadFile = File(...)):
# 实现可选参数，可以将参数的默认值设置为None。例如：
    # 对于表单字段：username: Optional[str] = Form(None)
    # 对于文件字段：file: Optional[UploadFile] = File(None)
# async def upload_file(username: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    file_content = await file.read()
    return {
        "username": username,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(file_content)
    }

def main():
    uvicorn.run(app="request_body_form_multipart:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()