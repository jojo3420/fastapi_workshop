from typing import List

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from telbot.schemas import Quiz, QuizCreate, ResourceId
from telbot.database import get_conn
from telbot import models

router = APIRouter()


async def add_quiz(
    conn: Session, question: str, examples: str, answer: int
) -> models.Quiz:
    quiz = models.Quiz(question=question, examples=examples, answer=answer)
    conn.add(quiz)
    conn.commit()
    return quiz


# /v1/quiz
@router.get("", response_model=List[Quiz])
def get_quiz_list(conn: Session = Depends(get_conn)):
    return conn.query(models.Quiz).all()


# /v1/quiz
@router.post("", response_model=ResourceId, status_code=status.HTTP_201_CREATED)
async def register_quiz(data: QuizCreate, conn: Session = Depends(get_conn)):
    return await add_quiz(conn=conn, **data.dict())


# /v1/quiz/form
@router.post("/form", response_model=ResourceId, status_code=status.HTTP_201_CREATED)
async def register_quiz_form(
    question: str = Form(..., title="퀴즈질문"),
    examples: str = Form(..., title="퀴즈 보기"),
    answer: int = Form(..., title="정답"),
    conn: Session = Depends(get_conn),
):
    return await add_quiz(conn, question, examples, answer)


# /v1/quiz/pic-one
@router.get("/pic-one", response_model=Quiz)
def pic_one_by_random(conn: Session = Depends(get_conn)):
    return conn.query(models.Quiz).order_by(func.RAND()).first()
