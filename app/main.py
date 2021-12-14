from typing import List

from fastapi import Depends, FastAPI, HTTPException, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import models
import schemas
from database import SessionLocal, engine

# models 구조에 따라 DB 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# /static 경로 생성과 static 자원 등록
# http://localhost:8000/static/login.html 접근가능
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exited_user = db.query(models.User).filter_by(email=user.email).first()
    if exited_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()

    return new_user


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# 핸들러에서 Form 매개변수로 받으니  요청시 application/x-www-form-urlencoded
# 알아서 설정된다.
@app.post("/login")  # response_model=schemas.User
def login_form(
    email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(email=email).first()
    if user:
        if user.password == password:
            return user
        return {"msg": "PASSWORD IS NOT MATCHING"}
    return {"msg": "USER NOT FOUND"}


@app.post("/signin")
def sign_in(
    email: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...),  # 파일로 받기..
):
    return {
        "email": email,
        "password": password,
        "filename": file.filename,
        "content_type": file.content_type,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
