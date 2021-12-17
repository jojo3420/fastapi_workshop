from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from devtools import debug


class ResourceId(BaseModel):
    id: int

    class Config:
        orm_mode = True


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


class QuizCreate(BaseModel):
    question: str = Field(..., title="퀴즈 질문", example="🇰🇷 대한민국의 수도는?")
    examples: str = Field(..., title="퀴즈 보기", example="1️⃣ 서울\n2️⃣ 인천\n3️⃣ 부산\n4️⃣ 대구")
    answer: int = Field(..., title="정답", example=1)


class Quiz(QuizCreate):
    id: int

    class Config:
        orm_mode = True
