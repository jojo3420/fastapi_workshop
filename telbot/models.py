from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    func,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Session
from devtools import debug

from telbot.database import Base
from telbot import schemas


# class IDMixin:
#     id = Column(Integer, primary_key=True, index=True)


class DateTimeMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )


class User(DateTimeMixin, Base):
    """sqlalchemy model USER Table"""

    __tablename__ = "user"

    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)


class Member(DateTimeMixin, Base):
    """sqlalchemy telegram member table"""

    __tablename__ = "member"

    is_bot = Column(Boolean, default=False)
    first_name = Column(String(15))
    last_name = Column(String(15))
    username = Column(String(30), nullable=True)
    language_code = Column(String(2), nullable=True)
    score = Column(Integer, default=0)

    quiz_id = Column(Integer, ForeignKey("quiz.id"))

    @staticmethod
    def save(conn: Session, member: schemas.Member):
        debug(member)
        row = Member(
            id=member.id,
            username=member.username,
            first_name=member.first_name,
            last_name=member.last_name,
            language_code=member.language_code,
        )
        conn.add(row)
        conn.commit()


class Quiz(DateTimeMixin, Base):
    """
    퀴즈 테이블
    """

    __tablename__ = "quiz"

    question = Column(Text, nullable=False)
    examples = Column(Text, nullable=False)
    answer = Column(Integer, nullable=False)

    member = relationship("Member")
