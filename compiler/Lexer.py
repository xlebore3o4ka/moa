from compiler.Errors import LexerError
from compiler.Token import Token
from compiler.TokenType import TokenType


class Lexer:
    MAX_REPETITIONS = 100000

    def __init__(self, text: str, file: str):
        self.text = text
        self.file = file

        self.pos = 0
        self.tokens: list[Token] = []
        self.error_stacktrace = []

        self.parenthesis = []

        self.col = 0
        self.line = 1

    def get(self, relative: int = 0) -> str:
        pos = self.pos + relative
        if pos >= len(self.text): return '\0'
        return self.text[pos]

    def next(self, times: int = 1) -> str:
        self.pos += times
        self.col += times
        return self.get()

    def add(self,
            type: TokenType,
            value: str,
            col: int = None,
            length: int = None,
            line: int = None,
            lexeme: str = None,
            ) -> None:
        col = col or self.col
        length = length or len(value)
        line = line or self.line
        lexeme = lexeme or self.text.split('\n')[line - 1]
        self.tokens.append(Token(type, value, length, col, line, lexeme, self.file))

    def tokenize(self) -> list[Token]:
        self.error_stacktrace.append("tokenize")

        prev = ''
        repetitions = 0

        while self.pos < len(self.text):
            c = self.get()

            if c in ' \t':
                self.skip_whitespace()
            elif c in TokenType.value(TokenType.NEWLINE):
                self.tokenize_newline()
            elif c in TokenType.group("OPERATORS") and not (
                    c == '.' and self.get(1) in TokenType.value(TokenType.NUMBER)):
                self.tokenize_operator()
            elif c in TokenType.value(TokenType.NUMBER):
                self.tokenize_number()
            else:
                raise LexerError("SyntaxError", f"Unexpected character '{c}'", self.col, self.line, 1,
                                 self.text.split('\n')[self.line - 1], self.file, self.error_stacktrace)

            repetitions += 1 if c == prev else -repetitions

            if repetitions >= self.MAX_REPETITIONS:
                raise LexerError(
                    "LexerError",
                    f"Too many repetitions of the same character >{self.MAX_REPETITIONS}\n  (most likely an endless loop)\n\n"
                    f"  This error occurred due to a bug in the code.\n  "
                    f"Write about this to the developer on our\n  discord server 'https://discord.gg/RFqmMKsDAZ'",
                    self.col, self.line, 1, self.text.split('\n')[self.line - 1], self.file, self.error_stacktrace
                )

            prev = c

        if self.parenthesis:
            raise LexerError.from_token("SyntaxError", f"'{self.parenthesis[-1].value}' was never closed",
                                        self.parenthesis[-1], self.error_stacktrace)

        self.error_stacktrace.pop()
        return self.tokens

    def skip_whitespace(self) -> None:
        while self.get() in ' \t':
            self.next()

    def tokenize_number(self) -> None:
        self.error_stacktrace.append("tokenize_number")
        number = ""
        col = self.col

        next_char = self.get()
        while next_char in TokenType.value(TokenType.NUMBER):
            number += next_char
            next_char = self.next()

        self.add(TokenType.NUMBER, number, col)

        if number.count('.') > 1: raise LexerError.from_token(
            "SyntaxError", "Too many dots in float number", self.tokens[-1], self.error_stacktrace)
        self.error_stacktrace.pop()

    def tokenize_operator(self) -> None:
        operator = ""
        col = self.col

        next_char = self.get()
        while operator + next_char in TokenType.group("OPERATORS"):
            operator += next_char
            next_char = self.next()

        self.add(TokenType.type(operator), operator, col)

        if operator in ['(', '[', '{']:
            self.parenthesis.append(self.tokens[-1])
        elif operator in [')', ']', '}']:
            if not self.parenthesis:
                raise LexerError.from_token("SyntaxError", f"Unmatched '{self.tokens[-1].value}'", self.tokens[-1],
                                            self.error_stacktrace)
            self.parenthesis.pop()

    def tokenize_newline(self) -> None:
        if not self.tokens or self.pos == len(self.text) - 1:
            while self.get() == '\n':
                self.next()
            self.col, self.line = 0, self.line + 1
            return

        if self.get() == ':':
            self.next()
            self.skip_whitespace()
            if self.get() == '\n':
                while self.get() == '\n':
                    self.next()
                return
            self.add(TokenType.NEWLINE, ':')
        else:
            self.col, self.line = 0, self.line + 1
            self.next()
            if self.tokens[-1].type != TokenType.NEWLINE:
                self.add(TokenType.NEWLINE, '\n')
