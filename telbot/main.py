from typing import List

from fastapi import FastAPI, Depends, Body, Request
from fastapi.staticfiles import StaticFiles
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from devtools import debug

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


@app.post("/webhook/register")
async def register_webhook_url(url: HttpUrl = Body(..., embed=True)):
    return await bot.set_webhook_url(url)


@app.get("/webhook/info")
async def get_webhook_info():
    return await bot.get_webhook_info()


@app.post("/webhook/receive")
async def receive_message(request: Request):
    data = await request.json()
    # debug(data)
    instance = schemas.Update.parse_obj(data)
    debug(instance)
    return "OK"


@app.get("/webhook/clearurl")
async def remove_all_url():
    return await bot.delete_webhook_url()


@app.get("/users", response_model=List[schemas.User])
def read_users(conn: Session = Depends(get_conn)):
    return conn.query(models.User).all()
