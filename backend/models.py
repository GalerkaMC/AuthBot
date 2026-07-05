"""
Pydantic модели для API
"""


from pydantic import BaseModel


class AuthRequest(BaseModel):
    """
    Запрос с сервера на 2FA
    """

    userId: str
    nickname: str
