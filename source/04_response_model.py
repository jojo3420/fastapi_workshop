import uvicorn
from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class User(BaseModel):
    name: str
    # password: str
    # avatar_url: Optional[HttpUrl] = None
    avatar_url = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users/me", response_model=User)
def get_user(user: User):
    # http POST :8000/users/me name=park
    return user


@app.post(
    "/users",
    response_model=User,  # 응답 모델
    # status_code=201  # 응답코드 201 Created
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: CreateUser):  # 요청모델
    # http POST :8000/users name=park password=1234
    # http POST :8000/users name=park password=1234 avatar_url=https://naver.com
    print("회원가입: ", user)
    return user


class Member(BaseModel):
    name = "fastapi"
    password: str
    avatar_url: HttpUrl = None


# @app.post(
#     '/include',
#     response_model=Member,
#     response_model_include=["name", "avatar_url"]
#     Set, List 타입도 괜찮음
# )
# def get_member_with_include(member: Member):
#     print('member: ', member)
#     return Member


if __name__ == "__main__":
    uvicorn.run("04_response_model:app", reload=True)
