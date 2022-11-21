"""Token related classes"""

from typing import Any, List


class Token:
    """Token class"""

    def __init__(self, token_type: Any = None, value: str = '') -> None:
        self.__Type = token_type
        self.__Value = value

    @property
    def type(self):
        """Retrieves the type of the token"""
        return self.__Type

    @property
    def value(self):
        """Retrieves the value of the token"""
        return self.__Value

    @value.setter
    def value(self, value: str):
        """Sets the value of the token"""
        self.__Value = value

    def __str__(self) -> str:
        return f'[{self.type}: {self.value}]'


class TokenList(List[Token]):
    """Token List Class"""

    def __str__(self) -> str:
        return "".join([str(t) for t in self])


__all__ = ["Token", "TokenList"]
