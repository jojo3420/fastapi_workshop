from pydantic import HttpUrl
from devtools import debug
from fastapi import APIRouter, Request, Body, Depends
from sqlalchemy.orm import Session
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
    # debug(update_ins)
    if update_ins.message:
        member: Member = update_ins.message.from_
        exist_member = conn.query(models.Member).filter_by(id=member.id).first()
        if not exist_member:
            models.Member.save(conn, member)

        chat = update_ins.message.chat
        text = update_ins.message.text
        if text in ["quiz", "문제", "질문"]:
            return await bot.send_quiz_msg(conn, chat.id, exist_member)
        if text.split(":")[0] in ["정답", "answer", "답"]:
            if exist_member.quiz_id:
                user_answer = int(text.split(":")[1])
                return await bot.send_quiz_result(
                    conn, chat.id, exist_member, user_answer
                )
        return await bot.send_quiz_intro(chat.id)


@router.delete("/url")
async def delete_all_url():
    return await bot.delete_webhook_url()


@router.post("/send/message")
async def send_message(message: str = Body(..., min_length=1)):
    return await bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID.get_secret_value(), message=message
    )
