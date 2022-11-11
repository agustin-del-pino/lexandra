from typing import Any


class Token:
    """Token class"""

    def __init__(self, token_type: Any = None, value: str = '') -> None:
        self.__Type = token_type
        self.__Value = value

    @property
    def type(self):
        """Retrives the type of the token"""
        return self.__Type

    @property
    def value(self):
        """Retrives the value of the token"""
        return self.__Value

    @value.setter
    def value(self, value: str):
        """Sets the value of the token"""
        self.__Value = value


__all__ = ["Token"]
