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


# ------------------------------------------------
# Enums
# ------------------------------------------------


class ChatType(str, Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"


# ------------------------------------------------
# Models
# ------------------------------------------------


class Member(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: Optional[str]
    language_code: Optional[str]


class Chat(BaseModel):
    id: int
    type: ChatType
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]


class Message(BaseModel):
    message_id: int
    from_: Optional[Member] = Field(None, title="sender", alias="from")
    date: datetime
    chat: Chat
    text: Optional[str] = Field(None, max_length=4096)


class Update(BaseModel):
    update_id: int
    message: Optional[Message]
