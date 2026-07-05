from abc import ABC, abstractmethod

from src.backend.two_factor_authentication.entities import Status


class ClientInterface(ABC):
    """Client interface"""

    @abstractmethod
    async def send_auth(self, user_id: int, payload: str) -> None:
        """Send auth request to client.
        :param user_id: player ID
        :param payload: Payload to return to backend after 2FA confirmation
        :return: None
        """

        pass

    @abstractmethod
    async def send_result(self, user_id: int, status: Status) -> None:
        """Send result to player.
        :param user_id: player ID
        :param status: result status
        :return: None
        """

        pass
