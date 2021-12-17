from typing import Union
from pydantic import SecretStr
from devtools import debug
import httpx
from httpx import Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from telbot import models


class TelegramBot:
    API_HOST = "https://api.telegram.org"

    def __init__(self, token: Union[str, SecretStr]) -> None:
        self._token = token
        self.client = httpx.AsyncClient(base_url=self.host)

    @property
    def token(self):
        if isinstance(self._token, SecretStr):
            return self._token.get_secret_value()
        return self._token

    @property
    def host(self):
        return f"{self.API_HOST}/bot{self.token}"

    async def get_bot_info(self):
        """get current bot info"""
        res = await self.client.get("/getMe")
        return res.json()

    async def get_webhook_info(self):
        """get webhook info"""
        res: Response = await self.client.get("/getWebhookInfo")
        # debug(res)
        return res.json()

    async def set_webhook_url(self, url: str):
        """set webhook response host url"""
        res: Response = await self.client.post("/setWebhook", data={"url": url})
        # debug(res)
        return res.json()

    async def delete_webhook_url(self):
        res: Response = await self.client.get("/deleteWebhook")
        return res.json()

    async def send_message(self, chat_id: str, message: str):
        """텔레그램 메시지 전송"""
        res: Response = await self.client.post(
            "/sendMessage",
            data={"chat_id": chat_id, "text": message},
        )
        return res.json()

    async def send_quiz_msg(self, conn: Session, chat_id, member):
        """퀴즈 봇 질문 사용자에게 메시지 전달하기"""
        quiz = conn.query(models.Quiz).order_by(func.RAND()).first()
        sent = await self.send_message(
            chat_id, message=f"{quiz.question}\n {quiz.examples}"
        )
        if sent.get("ok") is True:
            member.quiz_id = quiz.id
            conn.commit()

    async def send_quiz_result(self, conn: Session, chat_id, member, user_answer):
        """퀴즈봇 정답 체크하기"""
        quiz = conn.query(models.Quiz).filter_by(id=member.quiz_id).first()
        member.score += 1
        msg = f"축하합니다. 정답입니다."
        if quiz.answer != user_answer:
            msg = f"아쉽지만 정답은 {quiz.answer}번 입니다."
            member.score -= 1
        sent = await self.send_message(chat_id=chat_id, message=msg)
        if sent.get("ok") is True:
            member.quiz_id = None
            conn.commit()

    async def send_quiz_intro(self, chat_id: str):
        """퀴즈봇 기본 안내 메시지 전송"""
        message = (
            "안녕하세요. 퀴즈봇입니다.\n "
            "퀴즈를 원하지면 [질문, 문제, quiz] 중에 입력해주세요.\n "
            "또는 정답을 맞추려면 정답: 숫자를 입력해주세요."
        )
        await self.send_message(chat_id=chat_id, message=message)
