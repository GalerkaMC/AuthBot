"""
Telegram bot client implementing ClientInterface via aiogram.
"""
import os

from aiogram import Bot, Dispatcher

from src.backend.two_factor_authentication.entities.status import Status
from src.client.ClientInterface import ClientInterface
from .messages import MESSAGES
from .routers import start_router, help_router, callbacks_router
from .routers.callbacks import auth_button


class TelegramBot(ClientInterface):
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("Telegram token not provided")
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        self._register_routers()

    def _register_routers(self):
        self.dp.include_router(start_router)
        self.dp.include_router(help_router)
        self.dp.include_router(callbacks_router)

    async def send_auth(self, user_id: int, jwt: str) -> None:
        """Send 2FA prompt with inline button containing JWT."""
        await self.bot.send_message(
            chat_id=user_id,
            text=MESSAGES["auth_prompt"],
            reply_markup=auth_button(jwt),
        )

    async def send_result(self, user_id, status: Status) -> None:
        """Send result based on Status enum."""
        mapping = {
            Status.successful: MESSAGES["result_successful"],
            Status.expired: MESSAGES["result_expired"],
            Status.illegal: MESSAGES["result_illegal"],
        }
        text = mapping.get(status, "Unknown status")
        await self.bot.send_message(chat_id=user_id, text=text)

    async def run(self):
        """Start polling. Use in async context or via asyncio.run()."""
        await self.dp.start_polling(self.bot)
