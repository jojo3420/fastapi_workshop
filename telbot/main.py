from typing import List

# import uvicorn

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from telbot import schemas
from telbot import models
from telbot.lib.telegram import TelegramBot
from telbot.config import settings
from telbot.database import get_conn

app = FastAPI()
bot = TelegramBot(settings.TELEGRAM_BOT_TOKEN)


@app.on_event("startup")
def startup():
    from telbot.database import engine

    app.mount("/static", StaticFiles(directory="static"), name="static")
    models.Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return "hello world"


@app.get("/me")
async def get_me():
    return await bot.get_bot_info()


@app.get("/users", response_model=List[schemas.User])
def read_users(conn: Session = Depends(get_conn)):
    return conn.query(models.User).all()
