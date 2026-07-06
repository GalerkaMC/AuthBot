from src.client.ClientInterface import ClientInterface

class ClientFabric:
    """
    Скрывает реализацию за интерфейсом и решает проблему циркулярных импортов

    Реализует Singleton, пример использования:
        ClientFabric().attribute_or_methor()
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(ClientFabric, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        self.__client = None

    def set_client(self, client):
        self.__client = client

    def get(self) -> ClientInterface:
        return self.__client
