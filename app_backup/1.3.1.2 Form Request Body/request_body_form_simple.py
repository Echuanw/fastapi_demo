import uvicorn

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# /路径返回一个HTML页面，其中包含一个表单。
# response_class=HTMLResponse 指定路由返回的是HTML内容。FastAPI会将返回的字符串作为HTML处理，并设置 Content-Type为text/html
@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Submit Form</title>
        </head>
        <body>
            <h1>Submit Form</h1>

            <p>
            表单使用POST方法提交数据到/submit/路径 <br>
            默认使用 application/x-www-form-urlencoded 作为 Content-Type <br>
            name="username" "password" 这个对应了给 submit_form 函数的参数名字
            </p>
            
            <form action="/submit/" method="post">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

# /submit/路径用于处理表单提交。
@app.post("/submit/")
async def submit_form(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

def main():
    uvicorn.run(app="request_body_form_simple:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == '__main__':
    main()