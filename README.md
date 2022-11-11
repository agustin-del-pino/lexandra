# Pylexer

Create a lexer by decorators.

# How to use it

```python
import pylexer as plx

lexer: pylexer.Lexer = plx.Lexer(
    numbers='0123456789'
)

@lexer.numbers
def lex_numbers(c: plx.Cursor, s: plx.Settings) -> plx.Token:
    t = plx.Token(
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
import pylexer as plx

numbs_lexer: plx.Lexer = plx.factory.numbs_lexer()
words_lexer: plx.Lexer = plx.factory.words_lexer()
custom_lexer: plx.Lexer = plx.factory.custom_lexer(
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

# Cool aplications with Pylexer

Create a highlight code in the terminal

```python
from typing import List
import pylexer as plx

class Colors:
    Black='\u001b[30m'
    Red='\u001b[31m'
    Green='\u001b[32m'
    Yellow='\u001b[33m'
    Blue='\u001b[34m'
    Magenta='\u001b[35m'
    Cyan='\u001b[36m'
    White='\u001b[37m'
    _Reset='\u001b[0m'

    @classmethod
    def colorize(cls, color: str, text: str) -> str:
        return f'{color}{text}{cls._Reset}'


json_lexer: plx.Lexer = plx.factory.custom_lexer(
    numbers=plx.factory.NUMBERS,
    words=plx.factory.LETTERS,
    strings='"',
    delimiters='{},:[]\n '
    allow_floats=True,
    allow_uppercase=True
)

highlight_colors = {
    plx.factory.NUMB_TOKEN: Colors.Blue,
    plx.factory.WORDS_TOKEN: Colors.Cyan,
    plx.factory.STR_TOKEN: Colors.Green,
    plx.factory.DLT_TOKEN: Color.White,
}

def highlight(tokens: List[plx.Token]) -> str:
    highlighted = ""

    for token in tokens:
        highlighted += Colors.colorize(highlight_colors[token.type], token.value)

    return highlighted


if __name__ == '__main__':
    tokens = json_lexer('''{
        "json":{
            "type": "array",
            "length": 5,
            "items": [true, false, "pylexer", 123456789]
        }
    }''')

    print(highlight(tokens))

```

Why not do the same but with CSS.

```python
from typing import List
from strings import Template
import base64 as b64
import webbrowser
import pylexer as plx

BASE_HTML = Template(f'''
<!DOCTYPE html>
<html>
<head>
    <title>JSON Highlight</title>
    <style>
    .token-{plx.factory.NUMB_TOKEN} {{
        color: blue;
    }}
    .token-{plx.factory.WORD_TOKEN} {{
        color: cyan;
    }}
    .token-{plx.factory.STR_TOKEN} {{
        color: green;
    }}
    .token-{plx.factory.DLT_TOKEN} {{
        color: magenta;
    }}
    </style>
</head>
<body>
    $CONTENT
</body>
</html>
''')


json_lexer: plx.Lexer = plx.factory.custom_lexer(
    numbers=plx.factory.NUMBERS,
    words=plx.factory.LETTERS,
    strings='"',
    delimiters='{},:[]\n '
    allow_floats=True,
    allow_uppercase=True
)

def highlight(tokens: List[plx.Token]) -> str:
    content = ""

    for token in tokens:
        content += f'<span class="token-{token.type}">{token.value}</span>'

    return base_html.substitute(content=content)


if __name__ == '__main__':
    tokens = json_lexer('''{
        "json":{
            "type": "array",
            "length": 5,
            "items": [true, false, "pylexer", 123456789]
        }
    }''')

    html = highlight(tokens).encode("utf-8")
    url = f'data:text/html;base64,{b64.urlsafe_b64encode(html)}'

    webbrowser.open(url)

```
