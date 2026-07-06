"""
Telegram bot client implementing ClientInterface via aiogram.
"""
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import dotenv

from src.client.ClientFabric import ClientFabric
from src.backend.two_factor_authentication.entities.status import Status
from src.client.ClientInterface import ClientInterface
from .messages import MESSAGES
from .routers import start_router, help_router, callbacks_router
from .routers.callbacks import auth_button


dotenv.load_dotenv(".env.telegram")


class TelegramBot(ClientInterface):
    """
    Класс реализует интерфейс клиент через Telegram-бота
    Реализует Singleton паттерн, использование:
         TelegramBot().attribute_or_method()
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(TelegramBot, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.init(*args, **kwargs)

    def init(self, token: str | None = None):
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("Telegram token not provided")
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self._register_routers()
        ClientFabric().set_client(self)


    def _register_routers(self):
        self.dp.include_router(start_router)
        self.dp.include_router(help_router)
        self.dp.include_router(callbacks_router)

    async def send_auth(self, user_id: int, payload: str) -> None:
        """Send 2FA prompt with inline button containing Pyaload."""
        await self.bot.send_message(
            chat_id=user_id,
            text=MESSAGES["auth_prompt"],
            reply_markup=auth_button(payload),
        )

    async def send_result(self, user_id: int, status: Status) -> None:
        """Send result based on Status enum."""
        mapping = {
            Status.successful: MESSAGES["result_successful"],
            Status.expired: MESSAGES["result_expired"],
            Status.illegal: MESSAGES["result_illegal"],
        }
        if status not in mapping:
            raise ValueError(f"Unsupported status: {status}")
        text = mapping[status]
        await self.bot.send_message(chat_id=user_id, text=text)

    async def run(self):
        """Start polling. Call within async context."""
        await self.dp.start_polling(self.bot, handle_signals=False)
