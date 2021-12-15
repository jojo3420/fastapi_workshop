from sqlalchemy import Boolean, Column, Integer, String
from telbot.database import Base


class User(Base):
    """sqlalchemy model USER Table"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
