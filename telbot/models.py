from sqlalchemy import Boolean, Column, Integer, String
from telbot.database import Base


class User(Base):
    """sqlalchemy model USER Table"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)


class Member(Base):
    """sqlalchemy telegram member table"""

    __tablename__ = "member"

    id = Column(Integer, primary_key=True)
    is_bot = Column(Boolean, default=False)
    first_name = Column(String(15))
    last_name = Column(String(15))
    username = Column(String(30), nullable=True)
    language_code = Column(String(2), nullable=True)
    score = Column(Integer, default=0)
