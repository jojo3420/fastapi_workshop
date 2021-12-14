from fastapi import FastAPI
from enum import Enum
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"msg": "home"}


@app.get("/qs")
def query_string_test(id: int, page: int = 1):
    # http :8000/qs id==10 page==5
    return {"id": id, "page": page}


@app.get("/users")
def who_are_u(is_admin: bool, page: int = 1):
    #  http :8000/users is_admin==True page==10
    print(is_admin, page)
    return {
        "is_admin": is_admin,
        "page": page,
    }


@app.get("/me")
def user(name: str, age: int):
    return {"name": name, "page": age}


class MemberLevel(str, Enum):
    A = "A"
    B = "B"
    C = "C"


@app.get("/member")
def get_member(grade: MemberLevel = MemberLevel.A):
    # http GET :8000/member grade==C

    # grade A, B, C 중에 하나
    return {"grade": grade}


if __name__ == "__main__":
    uvicorn.run("02_querystring:app", reload=True)
