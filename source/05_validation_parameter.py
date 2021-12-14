import uvicorn
from typing import List
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

# 파라미터 검증
# 1) Fastapi validation 이용하는 방법 => Query, Path 검증할때 사용
# 2) pydantic 모델에 validation 이용하는 방법 => requestBody 검증


app = FastAPI()

db = [
    {"id": 1, "item_id": 1111, "name": "감자", "price": 300_000.0, "amount": 10},
    {"id": 2, "item_id": 2222, "name": "고구마", "price": 500_000.5, "amount": 5},
    {"id": 3, "item_id": 1111, "name": "감자칩", "price": 2_000.0, "amount": 1},
]


@app.get("/")
def home():
    return {"msg": "hello"}


class Item(BaseModel):
    name: str
    price = 0.0
    amount = 0


@app.get("/item/{item_id}/inventory", response_model=List[Item])
def get_item(
    # path variable
    # ... => 필수값 뜻함
    item_id: int = Path(..., gt=500, description="DB의 아이템 아이디"),
    # queryString
    # None => 옵션 뜻함
    name: str = Query(None, min_length=1, max_length=2, description="아이템 이름"),
):
    # http GET :8000/item/1111/inventory
    # http GET :8000/item/499/inventory name==감자칩   <= validation 예외
    # http GET :8000/item/1111/inventory name==감자
    # http GET :8000/item/1111/inventory name==감자칩  <=  max validation 예외

    items = []
    for item in db:
        if item.get("item_id") == item_id:
            items.append(item)

    if isinstance(name, str):
        response = []
        for _item in items:
            if _item.get("name") == name:
                response.append(_item)
                break
        return response

    return items


class Member(BaseModel):
    name: str = Field(..., min_length=2, max_length=6, title="이름")  # 필수값 2~6 사이값
    age: int = Field(..., gt=0)  # 필수값, 0보다 큼
    address: str = Field(None, title="주소")
    children_cnt: int = Field(
        defualt=0, gt=-1, le=10, title="자녀수", description="자녀의 수는 0에서 10 사이에 값 가짐"
    )


@app.post("/member/{id}")
def create_member(member: Member):
    #  http POST :8000/member/1 age=5 children_cnt=1 name=park
    #  http POST :8000/member/1 age=10 children_cnt=-1 name=park  # 파람 검증통과 실패
    #  http POST :8000/member/1 age=23 children_cnt=10 name=p  # 파람 검증통과 실패
    return member


if __name__ == "__main__":
    uvicorn.run("05_validation_parameter:app", reload=True)
