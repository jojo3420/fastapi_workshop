import uvicorn
from fastapi import FastAPI, Cookie, Header
from pydantic import BaseModel

app = FastAPI()


@app.get("/get_cookie")
def get_cookie(
    ga: str = Cookie(None),
    # ga: str = Cookie(...)
):
    # 쿠키 ga 는 필수가 아니므로 None
    # 쿠키 ga 는 필수 ...
    # http -v GET :8000/get_cookie Cookie:ga=adfs123.afsf
    # http -v GET :8000/get_cookie Cookie:ga=abc.cde.efg
    # http -v GET :8000/get_cookie
    return {
        "cookie_ga": ga,
    }


@app.get("/header")
def get_header(x_token: str = Header(..., title="api token")):
    # x_token 필수아님 => None
    # x_token 필수=> ...
    # http -v GET :8000/header X-Token:some.token.aa
    # http -v GET :8000/header  <== 예외발생

    return {"x_token": x_token}


if __name__ == "__main__":
    uvicorn.run("06_header_cookie:app", reload=True)
