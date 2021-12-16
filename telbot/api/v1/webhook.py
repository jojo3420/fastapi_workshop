from pydantic import HttpUrl
from devtools import debug
from fastapi import APIRouter, Request, Body, Depends
from sqlalchemy.orm import Session

from telbot import schemas
from telbot import models
from telbot.database import get_conn
from telbot.lib.telegram.telegram import TelegramBot
from telbot.config import settings
from telbot.lib.telegram.schema import Update, Member

bot = TelegramBot(settings.TELEGRAM_BOT_TOKEN)

router = APIRouter()


@router.get("/me")
async def get_bot_info():
    return await bot.get_bot_info()


@router.post("/register")
async def register_webhook_url(url: HttpUrl = Body(..., embed=True)):
    return await bot.set_webhook_url(url)


@router.get("/info")
async def get_webhook_info():
    return await bot.get_webhook_info()


@router.post("/receive")
async def receive_message(request: Request, conn: Session = Depends(get_conn)):
    data = await request.json()
    update_ins = Update.parse_obj(data)
    debug(update_ins)
    member: Member = update_ins.message.from_
    exist_member = conn.query(models.Member).filter_by(id=member.id).first()
    if not exist_member:
        row = models.Member(
            id=member.id,
            username=member.username,
            first_name=member.first_name,
            last_name=member.last_name,
            language_code=member.language_code,
        )
        conn.add(row)
        conn.commit()

    return "OK"


@router.delete("/url")
async def delete_all_url():
    return await bot.delete_webhook_url()
