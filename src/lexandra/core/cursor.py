"""Cursor Module"""


class Cursor:
    """Cursor class for read the text at lexer"""

    def __init__(self, content: str) -> None:
        self.__Content = content
        self.__Length = len(content)
        self.__Position = 0
        self.__Char = None

    @property
    def char(self):
        """Retrieves the current char"""
        return self.__Char

    @property
    def has_char(self):
        """Indicates there are still chars to read"""
        return self.__Char is not None

    @property
    def position(self):
        """Retrieves the current position"""
        return self.__Position

    def advance(self):
        """Advance to the next char"""
        if self.__Position < self.__Length:
            self.__Char = self.__Content[self.__Position]
            self.__Position += 1
        else:
            self.__Char = None


__all__ = ["Cursor"]
