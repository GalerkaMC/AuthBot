from abc import ABC, abstractmethod


class ITwoFAEntity(ABC):
    """Contract for 2FA attempt entities."""

    @property
    @abstractmethod
    def nickname(self) -> str:
        """Player nickname."""
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        """Telegram user ID."""
        pass

    @property
    @abstractmethod
    def created_at(self) -> float:
        """Timestamp of entity creation."""
        pass

    @abstractmethod
    async def send_2fa_message(self) -> None:
        """Send 2FA message to player."""
        pass

    @abstractmethod
    async def confirm(self) -> None:
        """Confirm successful login."""
        pass
