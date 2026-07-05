"""
Менеджер сущностей попыток 2FA
"""

import typing

import cachetools

from src.backend.two_factor_authentication.entities import ITwoFAEntity


class TwoFAEntitiesManager:
    """
    Менеджер сущностей попыток 2FA,
    Хранит и управляет объектами TwoFAEntity.

    Реализует Singleton паттерн, использование:
        TwoFAEntitiesManager().attribute_or_method()
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(TwoFAEntitiesManager, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        # Структура для хранения сущностей в формате ключ (ID) значение (TwoFAEntity)
        self.__entities: cachetools.LRUCache = cachetools.LRUCache(maxsize=100)

    def add(self, user_id: int, entity: ITwoFAEntity) -> None:
        """
        Добавить сущность в менеджере

        :param user_id: ID пользователя
        :param entity: Сущность
        :return: None
        """

        self.__entities[user_id] = entity

    def remove(self, user_id: int) -> None:
        """
        Удалить сущность из менеджера

        :param user_id: ID пользователя
        :return: None
        """

        del self.__entities[user_id]

    def get(self, user_id) -> typing.Optional[ITwoFAEntity]:
        """
        Получить сущность по ID

        :param user_id: ID пользователя
        :return: сущность, если она есть в менеджере, иначе None
        """

        return self.__entities.get(user_id)
