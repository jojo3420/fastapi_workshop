from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        # !!! 중요 !!!
        # pydantic  과 sqlalchemy 연동
        orm_mode = True
