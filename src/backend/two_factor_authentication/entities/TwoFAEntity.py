import time

from src.backend.two_factor_authentication.entities import TwoFAEntitiesManager
from src.backend.two_factor_authentication.entities import ITwoFAEntity
from src.backend.two_factor_authentication.entities import Status
from src.client.telegram.TelegramBot import TelegramBot

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
        await TelegramBot().send_auth(self.user_id, payload)

    async def confirm(self) -> None:
        """
        Подтвердить вход
        :return: None
        """

        result = await self.__request_2fa()
        await TelegramBot().send_result(self.__user_id, result)

    async def __request_2fa(self, *args) -> Status:
        """
        Запрос на сервер

        :param args:
        :return: Статус запроса
        """

        return Status.successful
