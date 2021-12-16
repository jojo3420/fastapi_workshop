from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from devtools import debug


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


class Member(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: Optional[str]
    language_code: Optional[str]
    score: int = Field(default=0)

    class Config:
        orm_mode = True
