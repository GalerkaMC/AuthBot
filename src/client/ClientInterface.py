from abc import ABC, abstractmethod

from src.backend.two_factor_authentication.entities import Status


class ClientInterface(ABC):
    """
    Интерфейс клиента
    """

    @abstractmethod
    async def send_auth(self, user_id: int, jwt: str) -> None:
        """
        Отправьте клиенту

        :param user_id: ID игрока
        :param jwt: JWT который нужно вернуть на backend при подтверждении 2FA игроком
        :return: None
        """

        pass

    @abstractmethod
    async def send_result(self, user_id, status: Status) -> None:
        """
        Отправить игроку ответ на подтверждение

        :param user_id: ID игрока
        :param status: ответ
        :return: None
        """

        pass
