"""Lexer's factory module"""

from typing import Callable
from lexandra.core import Lexer, Settings, Cursor, Token
from lexandra.utils import char_range
from lexandra.factory import constants


def _lex_numbs_float(cursor: Cursor, settings: Settings):
    token = Token(token_type=constants.NUMB_TOKEN, value=cursor.char)

    cursor.advance()

    while cursor.has_char and (cursor.char in settings.numbers or cursor.char == '.'):
        if cursor.char == '.' and '.' in token.value:
            token.type = constants.FLT_TOKEN
            break
        token.value += cursor.char
        cursor.advance()

    return token


def _lex_numbs(cursor: Cursor, settings: Settings) -> Token:
    token = Token(token_type=constants.NUMB_TOKEN, value=cursor.char)

    cursor.advance()

    while cursor.has_char and cursor.char in settings.numbers:
        token.value += cursor.char
        cursor.advance()

    return token


def _lex_string(cursor: Cursor, settings: Settings):
    token = Token(token_type=constants.STR_TOKEN, value=cursor.char)

    cursor.advance()

    while cursor.has_char:
        if cursor.char in settings.strings:
            token.value += cursor.char
            break

        token.value += cursor.char
        cursor.advance()

    cursor.advance()

    return token


def _lex_words(cursor: Cursor, predicate: Callable[[str], bool]) -> Token:
    token = Token(token_type=constants.WORD_TOKEN, value=cursor.char)

    cursor.advance()

    while cursor.has_char and predicate(cursor.char):
        token.value += cursor.char
        cursor.advance()

    return token


def _lex_words_only_letters(cursor: Cursor, settings: Settings) -> Token:
    return _lex_words(cursor, lambda ch: ch in settings.letters)


def _lex_words_alpha_num(cursor: Cursor, settings: Settings) -> Token:
    return _lex_words(cursor, lambda ch: ch in settings.letters or ch in settings.numbers)


def _lex_delimiters(cursor: Cursor, _: Settings):
    token = Token(token_type=constants.DLT_TOKEN, value=cursor.char)
    cursor.advance()
    return token


def custom_lexer(
    numbers: str = '',
    letters: str = '',
    delimiters: str = '',
    strings: str = '',
    ignores: str = '',
    allow_uppercase: bool = False,
    allow_float: bool = False,
    allow_numbers_in_words: bool = False,
    ignore_space: bool = False,
    ignore_newline: bool = False,
) -> Lexer:
    """Creates a custom lexer"""

    ignores += ('\n')*ignore_space +\
        (" ")*ignore_newline

    letters = letters+(letters.upper() if allow_uppercase else '')

    lexer = Lexer(
        Settings(
            numbers=numbers,
            letters=letters,
            strings=strings,
            delimiters=delimiters,
            ignores=ignores
        )
    )

    if numbers:
        if allow_float:
            lexer.numbers(_lex_numbs_float)
        else:
            lexer.numbers(_lex_numbs)

    if strings:
        lexer.strings(_lex_string)

    if letters:
        if allow_numbers_in_words:
            lexer.words(_lex_words_alpha_num)
        else:
            lexer.words(_lex_words_only_letters)

    if delimiters:
        lexer.delimiters(_lex_delimiters)

    return lexer


def numbs_lexer(ignore_non_numbs: bool = True, allow_float: bool = False):
    """Creates a lexer able to read numbers"""
    return custom_lexer(
        numbers=constants.NUMBERS,
        allow_float=allow_float,
        ignores=f'{char_range(int(0x00), int(0x29))}'
        f'{char_range(int(0x40), int(0xFF))}' if ignore_non_numbs else ' '
    )


def words_lexer(allow_uppercase: bool = False, allow_numbers_in_words: bool = False):
    """Creates a lexer able to read words"""
    return custom_lexer(
        letters=constants.LETTERS,
        allow_uppercase=allow_uppercase,
        allow_numbers_in_words=allow_numbers_in_words,
        ignore_space=True
    )


__all__ = [
    "custom_lexer", "numbs_lexer", "words_lexer"
]
