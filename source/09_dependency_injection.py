from typing import Any, Optional, Dict
import random
import string

import uvicorn
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# items = []
# for _ in range(1000):
#     name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
#     items.append({'name': name})


items = [
    {"name": "A"},
    {"name": "B"},
    {"name": "C"},
    {"name": "D"},
    {"name": "E"},
]


# 1) 함수스타일 DI
async def func_params(
    q: Optional[str] = None, offset: int = 0, limit: int = 100
) -> Dict[str, Any]:
    print(q, type(q))
    return {"q": q, "offset": offset, "limit": limit}


# DI 사용
@app.get("/pagination")
async def pagination(params: dict = Depends(func_params)):
    offset = params.get("offset", 0)
    limit = params.get("limit", 0)
    return {"q": params.get("q"), "items": items[offset : offset + limit]}


# 2) 클래스 스타일 DI
class ClassParams:
    def __init__(self, q: Optional[str] = None, offset: int = 0, limit: int = 100):
        self.q = q
        self.offset = offset
        self.limit = limit


@app.get("/pagination/class")
async def pagination_class(params: ClassParams = Depends(ClassParams)):
    offset, limit = params.offset, params.limit
    print(offset, limit)
    return {"q": params.q, "items": items[offset : offset + limit]}


# 3) Pydantic 스타일
class PydanticParams(BaseModel):
    # 파라미터 제약조건(검증) 가능해짐.
    q: Optional[str] = Field(None, min_length=2)
    offset: int = Field(0, ge=0)  # ge: Greater or Equal (크거나 같음) >=
    limit: int = Field(100, gt=0)  # Greater Than  0 크거나 (>)


@app.get("/pagination/pydantic")
async def pagination_pydantic(params: PydanticParams = Depends(PydanticParams)):
    offset, limit = params.offset, params.limit
    return {"q": params.q, "items": items[offset : offset + limit]}


# DI안에서 DI 사용하기
async def get_q(q: Optional[str] = None) -> Optional[str]:
    return q


async def func_params_with_sub(
    q: Optional[str] = Depends(get_q),  # DI 함수 안에서 DI 함수 사용
    offset: int = 0,
    limit: int = 100,
) -> Dict[str, Any]:
    return {"q": q, "offset": offset, "limit": limit}


@app.get("/pagination/didi")
async def pagination_di_di(params: dict = Depends(func_params_with_sub)):
    offset = params.get("offset")
    limit = params.get("limit")
    return {"q": params.get("q"), "items": items[offset : offset + limit]}


class XTokenHeader(BaseModel):
    x_token: str = Field(..., min_length=5, max_length=20)


async def verify_token(x_token: str = Header(...)) -> None:
    if len(x_token) < 10:
        raise HTTPException(401, detail="Not Allow Authorization")


# Router 데코레이터의 DI
# 라우터에서 dependencies = [Depends() ]
@app.get("/router1", dependencies=[Depends(XTokenHeader)])
async def router1():
    return items


@app.get("/router2", dependencies=[Depends(verify_token)])
async def router2():
    return items


if __name__ == "__main__":
    uvicorn.run("09_dependency_injection:app", reload=True)
