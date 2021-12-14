from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()


@app.get("/")
def main():
    return {"msg": "hello world"}


@app.get("/users/me")
def get_current_user():
    # 위로 올려짐..
    return {"user": "me"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    print(f"this is /user/{user_id}")
    return {"user_id": user_id}


@app.get("/log/{user_id}")
def log_client(user_id: float, request: Request):  # fastapi Request
    print(request.path_params)
    print(request)
    return {"user_id": user_id}


# # fast api 단점
# # fast api에서는 위아래 아래로 실행됨..
# 위에 /users/{user_id} 핸들러가 먼저 catch 하여 응답해버림
# 이 코드를 /users/{user_id} 위레 올려야 한다..
# @app.get('/users/me')
# def get_current_user():
#     return {'user': 'mr. park'}


if __name__ == "__main__":
    # 모듈이름:FastAPI Instance이름
    uvicorn.run("01_hello_world:app", reload=True)
