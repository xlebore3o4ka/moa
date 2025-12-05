from compiler.Token import Token


class Error(Exception):
    def __init__(self,
                 type: str,
                 message: str,
                 col: int,
                 line: int,
                 length: int,
                 lexeme: str,
                 file: str,
                 from_: str,
                 error_stacktrace: list
                 ) -> None:
        self.type = type
        self.message = message
        self.col = col
        self.line = line
        self.length = length
        self.lexeme = lexeme
        self.file = file
        self.from_ = from_
        self.error_stacktrace = error_stacktrace
        self.print_error()

    def print_error(self):
        print(f"Error in {repr(self.file + f":{self.line}:{self.col}")} for the reason:")
        for n, method in enumerate(self.error_stacktrace[::-1]):
            print(f"  from '{self.from_}.{method}'")
        print(f"  from '{self.from_}'")
        print(f"  {'':<{len(str(self.line))}} |")
        print(f"  {self.line} |  {self.lexeme}")
        print(f"  {'':<{len(str(self.line))}} |  {' ' * self.col}{'^' * self.length}")
        print(f"  {'':<{len(str(self.line))}} V")
        print(f"[{self.type}] {self.message}")


class LexerError(Error):
    @classmethod
    def from_token(cls,
                   type: str,
                   message: str,
                   token: Token,
                   stacktrace: list):
        return cls(type,
                   message,
                   token.col,
                   token.line,
                   token.length,
                   token.lexeme,
                   token.file,
                   stacktrace)

    def __init__(self,
                 type: str,
                 message: str,
                 col: int,
                 line: int,
                 length: int,
                 lexeme: str,
                 file: str,
                 stacktrace: list) -> None:
        super().__init__(type, message, col, line, length, lexeme, file, "Lexer", stacktrace)


class ParserError(Error):
    @classmethod
    def from_token(cls,
                   type: str,
                   message: str,
                   token: Token,
                   stacktrace: list):
        return cls(type,
                   message,
                   token.col,
                   token.line,
                   token.length,
                   token.lexeme,
                   token.file,
                   stacktrace)

    def __init__(self,
                 type: str,
                 message: str,
                 col: int,
                 line: int,
                 length: int,
                 lexeme: str,
                 file: str,
                 stacktrace: list) -> None:
        super().__init__(type, message, col, line, length, lexeme, file, "Parser", stacktrace)


class CompilerError(Error):
    @classmethod
    def from_token(cls,
                   type: str,
                   message: str,
                   token: Token,
                   node: str):
        return cls(type,
                   message,
                   token.col,
                   token.line,
                   token.length,
                   token.lexeme,
                   token.file,
                   node)

    def __init__(self,
                 type: str,
                 message: str,
                 col: int,
                 line: int,
                 length: int,
                 lexeme: str,
                 file: str,
                 node: str) -> None:
        super().__init__(type, message, col, line, length, lexeme, file, "Compiler", [f"{node}.compile"])

