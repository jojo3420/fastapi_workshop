from typing import List
from sqlalchemy.orm import Session
from devtools import debug

from fastapi import APIRouter, Depends

from telbot import schemas
from telbot import models
from telbot.database import get_conn

router = APIRouter()


@router.get("", response_model=List[schemas.User])
def read_users(conn: Session = Depends(get_conn)):
    return conn.query(models.User).all()
