from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from telbot.config import settings

url = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_SCHEMA}"
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_conn():
    """create session and return db conn"""
    conn = SessionLocal()
    try:
        yield conn
    finally:
        conn.close()
