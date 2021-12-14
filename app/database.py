from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import load_env

env: dict = load_env('env.json')

user = env.get('USER')
password = env.get('PASSWORD')
schema = env.get('SCHEMA')
host = env.get('HOST')
port = env.get('PORT')

url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

engine = create_engine(url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
