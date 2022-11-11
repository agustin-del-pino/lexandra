"""Lexer Module"""


from typing import List
from .token import Token
from .cursor import Cursor


class Settings:
    """Setting class for Lexer configuration"""

    def __init__(self, numbers: str = '',
                 letters: str = '',
                 strings: str = '',
                 delimiters: str = '',
                 ignores: str = '') -> None:

        self.__Numbers = numbers
        self.__Letters = letters
        self.__Strings = strings
        self.__Delimiters = delimiters
        self.__Ignores = ignores

    @property
    def numbers(self) -> str:
        """Retrives the numbers"""
        return self.__Numbers

    @property
    def letters(self) -> str:
        """Retrives the letters"""
        return self.__Letters

    @property
    def strings(self) -> str:
        """Retrives the strings"""
        return self.__Strings

    @property
    def delimiters(self) -> str:
        """Retrives the delimiters"""
        return self.__Delimiters

    @property
    def ignores(self) -> str:
        """Retrives the ignores"""
        return self.__Ignores


class LexerError(Exception):
    def __init__(self, *args: object) -> None:
        super(LexerError, self).__init__(*args)


class Lexer:
    """Lexer class for create a new empty lexer"""

    def __init__(self, settings: Settings) -> None:
        self.__Settings = settings

        self.__LexNumber = self.__LexWords = self.__LexStrings = self.__LexDelimiters = None

    def numbers(self, func):
        """Decorator for numbers"""
        self.__LexNumber = func

    def words(self, func):
        """Decorator for words"""
        self.__LexWords = func

    def strings(self, func):
        """Decorator for strings"""
        self.__LexStrings = func

    def delimiters(self, func):
        """Decorator for delimiters"""
        self.__LexDelimiters = func

    def _extended_lex(self, cursor: Cursor, tokens: List[Token]) -> bool:
        """Abstract method. For extend the call of the lexer"""
        return False

    def __call__(self, text: str) -> List[Token]:
        """Execute the lexer"""

        cursor = Cursor(text)
        tokens: List[Token] = []

        cursor.advance()

        while cursor.has_char:
            if cursor.char in self.__Settings.ignores:
                cursor.advance()
                continue
            elif cursor.char in self.__Settings.numbers:
                tokens.append(self.__LexNumber(cursor, self.__Settings))

            elif cursor.char in self.__Settings.strings:
                tokens.append(self.__LexStrings(cursor, self.__Settings))

            elif cursor.char in self.__Settings.letters:
                tokens.append(self.__LexWords(cursor, self.__Settings))

            elif cursor.char in self.__Settings.delimiters:
                tokens.append(self.__LexDelimiters(cursor, self.__Settings))

            elif not self._extended_lex(cursor, tokens):
                raise LexerError(
                    f'Unexcepted char {cursor.char} at position {cursor.position}')

        return tokens


__all__ = ["Lexer", "LexerError", "Settings"]
