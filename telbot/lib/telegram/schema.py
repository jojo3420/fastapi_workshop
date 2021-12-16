from typing import Optional
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field


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
