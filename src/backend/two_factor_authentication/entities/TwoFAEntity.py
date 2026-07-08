import logging
import time
import os

import aiohttp
import dotenv

from src.backend.two_factor_authentication.entities import TwoFAEntitiesManager
from src.backend.two_factor_authentication.entities import ITwoFAEntity
from src.backend.two_factor_authentication.entities import Status
from src.client.ClientFabric import ClientFabric


dotenv.load_dotenv(".env.config")
logger = logging.getLogger("bot")

class TwoFAEntity(ITwoFAEntity):
    """
    Сущность хранящая информацию о попытке 2FA

    nickname: str - Никнейм игрока
    user_id: int - ID игрока в Telegram
    created_at: float - Время создания попытки 2FA

    """
    def __init__(self, nickname: str, user_id: int) -> None:
        self.__nickname: str = nickname
        self.__user_id: int = user_id
        self.__created_at: float = time.time()

        # Сущность регистрируется в менеджере
        TwoFAEntitiesManager().add(self.__user_id, self)

    @property
    def nickname(self) -> str:
        return self.__nickname

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def created_at(self) -> float:
        return self.__created_at

    async def send_2fa_message(self) -> None:
        """
        Отправить попытку 2FA игроку
        :return: None
        """

        # Телеграмм гарантирует, что подделать userId невозможно
        # Замените payload например на JWT, для безопасности, если это понадобится
        payload = str(self.__user_id)
        await ClientFabric().get().send_auth(self.user_id, payload)

    async def confirm(self) -> None:
        """
        Подтвердить вход
        :return: None
        """

        result = await self.__request_2fa()
        await ClientFabric().get().send_result(self.__user_id, result)
        TwoFAEntitiesManager().remove(self.__user_id)

    async def __request_2fa(self) -> Status:
        """
        Запрос на сервер

        :return: Статус запроса
        """

        api_token = os.getenv("HOST_API_KEY")
        base_url = os.getenv("MINECRAFT_SERVER_BASE_URL")
        confirmation_url = os.getenv("CONFIRMATION_URL")
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": api_token
        }

        request_body = {
            'userId': str(self.__user_id),
            'nickname': self.__nickname,
            'status': "approved"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{base_url}{confirmation_url}",
                        headers=headers,
                        json=request_body) as response:

                    if response.status == 200:
                        return Status.successful

                    if response.status == 409:
                        return Status.expired

                    else:
                        logger.error(f"Confirmation request failed, content: {await response.text()}")
                        return Status.unexpected_exception

        except aiohttp.ClientError as e:
            logger.error("Confirmation request failed", e.args, e.__repr__())
            return Status.unexpected_exception
