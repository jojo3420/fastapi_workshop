from typing import Union
from pydantic import SecretStr
from devtools import debug
import httpx
from httpx import Response


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
