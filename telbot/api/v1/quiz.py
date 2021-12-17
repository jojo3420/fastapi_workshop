from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from telbot.schemas import Quiz, QuizCreate, ResourceId
from telbot.database import get_conn
from telbot import models

router = APIRouter()


@router.get("", response_model=List[Quiz])
def get_quiz_list(conn: Session = Depends(get_conn)):
    return conn.query(models.Quiz).all()


@router.post("", response_model=ResourceId)
def register_quiz(data: QuizCreate, conn: Session = Depends(get_conn)):
    quiz = models.Quiz(**data.dict())
    conn.add(quiz)
    conn.commit()
    return quiz


@router.get("/pic-one", response_model=Quiz)
def pic_one_by_random(conn: Session = Depends(get_conn)):
    return conn.query(models.Quiz).order_by(func.RAND()).first()
