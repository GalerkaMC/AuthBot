from enum import Enum


class Status(Enum):
    expired = "expired"
    successful = "successful"
    illegal = "illegal"
    unexpected_exception = "unexpected_exception"