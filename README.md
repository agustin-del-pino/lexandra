# Lexandra

Create a lexer by decorators.

# How to use it

```python
import lexandra.core as lxd

lexer: lxd.Lexer = lxd.Lexer(
    numbers='0123456789'
)

@lexer.numbers
def lex_numbers(c: lxd.Cursor, s: lxd.Settings) -> lxd.Token:
    t = lxd.Token(
        type='number',
        value=c.char
    )

    c.advance()

    while c.char in s.numbers:
        t.value += c.char
        c.advance()

    return t


if __name__ == '__main__':
    print(lexer('123'))
```

# Factory

Too much work? Use the factory for predefined lexers.

```python
import lexandra as lxd

numbs_lexer: lxd.Lexer = lxd.factory.numbs_lexer()
words_lexer: lxd.Lexer = lxd.factory.words_lexer()
custom_lexer: lxd.Lexer = lxd.factory.custom_lexer(
    numbers='0123456789',
    words='qwertyuiopasdfghjklñzxcvbnm',
    allow_uppercase=True,
    ignore_space=True
)


if __name__ == '__main__':
    print(numbs_lexer('123 456 789 0'))
    print(words_lexer('Hello World'))
    print(custom_lexer('Hello 123 World 456'))

```

# Cool stuffs with lexandra

Create a highlight code in the terminal

```python
import lexandra as lxd


class Colors:
    Black = '\u001b[30m'
    Red = '\u001b[31m'
    Green = '\u001b[32m'
    Yellow = '\u001b[33m'
    Blue = '\u001b[34m'
    Magenta = '\u001b[35m'
    Cyan = '\u001b[36m'
    White = '\u001b[37m'
    _Reset = '\u001b[0m'

    @classmethod
    def colorize(cls, color: str, text: str) -> str:
        return f'{color}{text}{cls._Reset}'


json_lexer: lxd.core.Lexer = lxd.factory.custom_lexer(
    numbers=lxd.factory.NUMBERS,
    letters=lxd.factory.LETTERS,
    strings='"',
    delimiters='{},:[]\n ',
    allow_float=True,
    allow_uppercase=True
)

highlight_colors = {
    lxd.factory.NUMB_TOKEN: Colors.Blue,
    lxd.factory.WORD_TOKEN: Colors.Cyan,
    lxd.factory.STR_TOKEN: Colors.Green,
    lxd.factory.DLT_TOKEN: Colors.White,
}


def highlight(tokens: lxd.core.TokenList) -> str:
    highlighted = ""

    for token in tokens:
        highlighted += Colors.colorize(
            highlight_colors[token.type], token.value)

    return highlighted


if __name__ == '__main__':
    tks = json_lexer('''{
        "json":{
            "type": "array",
            "length": 5,
            "items": [true, false, "lexandra", 123456789]
        }
    }''')

    print(highlight(tks))

```

Why not do the same but with CSS. No new lexer is needed, just replace the ASCII Color by HTML/CSS.

```python
from string import Template
import base64 as b64
import webbrowser
import lexandra as lxd

BASE_HTML = Template(f'''
<!DOCTYPE html>
<html>
<head>
    <title>JSON Highlight</title>
    <style>
    * {{
        white-space: pre-wrap;
        font-size: 30px;
        font-family: monospace;
    }}
    body {{
        background-color: #2e2e2e;
        border: 1px solid white;
        border-radius: 5px;
        width: fit-content;
        padding: 30px;
        margin: 0 auto;
    }}
    .token-{lxd.factory.NUMB_TOKEN} {{
        color: blue;
    }}
    .token-{lxd.factory.WORD_TOKEN} {{
        color: cyan;
    }}
    .token-{lxd.factory.STR_TOKEN} {{
        color: green;
    }}
    .token-{lxd.factory.DLT_TOKEN} {{
        color: magenta;
    }}
    </style>
</head>
<body>
    $content
</body>
</html>
''')


json_lexer: lxd.core.Lexer = lxd.factory.custom_lexer(
    numbers=lxd.factory.NUMBERS,
    letters=lxd.factory.LETTERS,
    strings='"',
    delimiters='{},:[]\n ',
    allow_float=True,
    allow_uppercase=True
)

def highlight(tokens: lxd.core.TokenList) -> str:
    content = ""

    for token in tokens:
        content += f'<span class="token-{token.type}">{token.value}</span>'

    return BASE_HTML.substitute(content=content)


if __name__ == '__main__':
    tokens = json_lexer('''{
        "json":{
            "type": "array",
            "length": 5,
            "items": [true, false, "lexandra", 123456789]
        }
    }''')

    html = highlight(tokens).encode("utf-8")
    url = f'data:text/html;base64,{b64.b64encode(html).decode("utf-8")}'

    webbrowser.open(url)

```

# Need more decorators? Just extends!.

```python
import lexandra as lxd


class MathSettings(lxd.core.Settings):
    def __init__(self, numbers: str, operators: str, letters: str = '', strings: str = '', delimiters: str = '', ignores: str = '') -> None:
        super(MathSettings, self).__init__(
            numbers, letters, strings, delimiters, ignores)

        self.__Operators = operators

    @property
    def operators(self):
        return self.__Operators


class MathLexer(lxd.core.Lexer):
    def __init__(self, settings: MathSettings) -> None:
        super(MathLexer, self).__init__(settings)
        self.__LexOperators = None

        # Workaround for typing (avoid the use of generic just for keep it simple)
        self._Settings = settings

    def operators(self, func: lxd.core.LexFunction):
        self.__LexOperators = func

    def _extended_lex(self, cursor: lxd.core.Cursor, tokens: lxd.core.TokenList) -> bool:
        # Extending the lex conditions

        if cursor.char in self._Settings.operators:
            tokens.append(self.__LexOperators(cursor, self._Settings))
            # The char is acceptable
            return True

        # The char is not acceptable
        return False


lexer: MathLexer = MathLexer(
    MathSettings("0123456789", "+-*/", ignores=" ")
)


@lexer.numbers
def lex_numbs(cursor: lxd.core.Cursor, settings: lxd.core.Settings) -> lxd.core.Token:
    token = lxd.core.Token(token_type="nums", value=cursor.char)

    cursor.advance()

    while cursor.has_char and cursor.char in settings.numbers:
        token.value += cursor.char
        cursor.advance()

    return token


@lexer.operators
def lex_ops(cursor: lxd.core.Cursor, _: lxd.core.Settings) -> lxd.core.Token:
    token = lxd.core.Token(token_type="mathop", value=cursor.char)
    cursor.advance()
    return token


if __name__ == "__main__":
    print(lexer("1234 + 5678 * 333 / 111 - 698"))

```