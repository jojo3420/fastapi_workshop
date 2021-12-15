from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()

# models 구조에 따라 DB 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# /static 경로 생성과 static 자원 등록
# http://localhost:8000/static/login.html 접근가능
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_conn():
    conn = SessionLocal()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/")
def index():
    return {"msg": "hello world"}


@app.get("/users", response_model=List[schemas.User])
def read_users(conn: Session = Depends(get_conn)):
    return conn.query(models.User).all()


if __name__ == "__main__":
    uvicorn.run("telbot.main:app", reload=True)
