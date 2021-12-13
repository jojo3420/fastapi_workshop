from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exited_user = db.query(models.User).filter_by(email=user.email).first()
    if exited_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()

    return new_user


@app.get('/users', response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
