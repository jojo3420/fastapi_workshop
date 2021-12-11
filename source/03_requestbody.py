from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
import uvicorn

app = FastAPI()


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None


class Item(BaseModel):
    name: str
    price: float
    amount: int = 0


class Member(BaseModel):
    name: str
    password: str
    inventory: List[Item] = []


@app.get('/me')
def get_me():
    # http GET :8000/me
    inventory = [
        Item(name='의류', price=500.0, amount=1),
        Item(name='자동차', price=1500.0, amount=2),
        Item(name='집', price=300.0, amount=5),
    ]
    fake_user = Member(name='park', password=1234,
                       inventory=inventory)
    return fake_user


@app.get('/member')
def get_member():
    # http GET :8000/member
    inventory = [
        Item(name='의류', price=500.0, amount=1),
        Item(name='자동차', price=1500.0, amount=2),
        Item(name='집', price=300.0, amount=5),
    ]
    fake_user = Member(name='park', password=1234,
                       inventory=inventory)
    return fake_user


@app.post('/member')
def create_member(member: Member):
    # http POST :8000/new/member name=park password=1234 inventory:='[{"name": "apple", "price": 20.1}, {"name": "banana", "price": 50.1, "amount": 5}]'
    return {
        'member': member
    }


@app.put('/member')
def update_member(member: Member):
    # http PUT :8000/member name=park password=123
    return {
        'member': member
    }


if __name__ == '__main__':
    uvicorn.run('03_requestbody:app', reload=True)
