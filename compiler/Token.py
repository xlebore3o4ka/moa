from compiler.TokenType import TokenType


class Token:
    def __init__(self,
                 type: TokenType,
                 value: str,
                 length: int,
                 col: int,
                 line: int,
                 lexeme: str,
                 file: str) -> None:
        self.type = type
        self.value = value
        self.length = length
        self.col = col
        self.line = line
        self.lexeme = lexeme
        self.file = file

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
