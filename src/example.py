import pylexer as plx

lexer: plx.Lexer = plx.Lexer(
    plx.Settings(
        numbers='0123456789',
        ignores=" "
    )
)


@lexer.numbers
def lex_numbers(cursor: plx.Cursor, settings: plx.Settings) -> plx.Token:
    """Lexs the numbers"""
    token = plx.Token(token_type="number", value=cursor.char)

    cursor.advance()

    while cursor.has_char and cursor.char in settings.numbers:
        token.value += cursor.char
        cursor.advance()

    return token


if __name__ == '__main__':
    print([f'[{token.type}: {token.value}]' for token in lexer('123 456 789 0')])
