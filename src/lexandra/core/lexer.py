"""Lexer Module"""


from typing import Callable, TypeVar
import lexandra.core.token as _Token
import lexandra.core.cursor as _Cursor


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
        """Retrieves the numbers"""
        return self.__Numbers

    @property
    def letters(self) -> str:
        """Retrieves the letters"""
        return self.__Letters

    @property
    def strings(self) -> str:
        """Retrieves the strings"""
        return self.__Strings

    @property
    def delimiters(self) -> str:
        """Retrieves the delimiters"""
        return self.__Delimiters

    @property
    def ignores(self) -> str:
        """Retrieves the ignores"""
        return self.__Ignores


class LexerError(Exception):
    """Lexer Error Class"""

    def __init__(self, *args: object) -> None:
        super(LexerError, self).__init__(*args)


LexFunction = TypeVar("LexFunction", bound=Callable[[_Cursor.Cursor], _Token.Token])


class Lexer:
    """Lexer class for create a new empty lexer"""

    def __init__(self, settings: Settings) -> None:
        self._Settings = settings

        self.__LexNumber = self.__LexWords = self.__LexStrings = self.__LexDelimiters = None

    def numbers(self, func: LexFunction):
        """Decorator for numbers"""
        self.__LexNumber = func

    def words(self, func: LexFunction):
        """Decorator for words"""
        self.__LexWords = func

    def strings(self, func: LexFunction):
        """Decorator for strings"""
        self.__LexStrings = func

    def delimiters(self, func: LexFunction):
        """Decorator for delimiters"""
        self.__LexDelimiters = func

    def _extended_lex(self, cursor: _Cursor.Cursor, tokens: _Token.TokenList) -> bool:
        """Abstract method. For extend the call of the lexer"""
        return False

    def __call__(self, text: str) -> _Token.TokenList:
        """Execute the lexer"""

        cursor = _Cursor.Cursor(text)
        tokens: _Token.TokenList = _Token.TokenList()

        cursor.advance()

        while cursor.has_char:
            if cursor.char in self._Settings.ignores:
                cursor.advance()
                continue

            if cursor.char in self._Settings.numbers:
                tokens.append(self.__LexNumber(cursor, self._Settings))

            elif cursor.char in self._Settings.strings:
                tokens.append(self.__LexStrings(cursor, self._Settings))

            elif cursor.char in self._Settings.letters:
                tokens.append(self.__LexWords(cursor, self._Settings))

            elif cursor.char in self._Settings.delimiters:
                tokens.append(self.__LexDelimiters(cursor, self._Settings))

            elif not self._extended_lex(cursor, tokens):
                raise LexerError(
                    f'Unexpected char {cursor.char} at position {cursor.position}')

        return tokens


__all__ = ["Lexer", "LexerError", "Settings", "LexFunction"]
