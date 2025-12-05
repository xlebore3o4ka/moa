from compiler.AST.BinaryExpression import BinaryExpression
from compiler.AST.Expression import Expression
from compiler.AST.FloatExpression import FloatExpression
from compiler.AST.IntExpression import IntExpression
from compiler.AST.UnaryExpression import UnaryExpression
from compiler.Errors import ParserError
from compiler.Token import Token
from compiler.TokenType import TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

        self.EOF = Token(TokenType.EOF, '', 1, (last_token := self.tokens[-1]).col + last_token.length + 1,
                         last_token.line, last_token.lexeme, last_token.file)
        self.parser_stacktrace = []

    def get(self, relative: int = 0) -> Token:
        pos = self.pos + relative
        if pos >= len(self.tokens): return self.EOF
        return self.tokens[pos]

    def next(self, times: int = 1) -> Token:
        self.pos += times
        return self.get()

    def look(self, *types: TokenType) -> bool:
        return any(self.get().type == type for type in types)

    def match(self, *types: TokenType) -> bool:
        if self.look(*types):
            self.next()
            return True
        return False

    def expect(self, *types: TokenType) -> Token | list[Token]:
        self.parser_stacktrace.append("expect")
        token = self.get()
        if self.match(*types):
            return token
        raise ParserError.from_token("SyntaxError",
                                     "Expected" + (" one of " if len(types) > 1 else " ") +
                                     ", ".join(map(str, types)) +
                                     f", got {self.get().type}",
                                     self.get(),
                                     self.parser_stacktrace)

    def parse(self) -> Expression:  # TODO: BlockStatement
        self.parser_stacktrace.append("parse")
        expression = self.expression()
        self.parser_stacktrace.pop()
        return expression

    def expression(self) -> Expression:
        self.parser_stacktrace.append("expression")
        expression = self.term_expression()
        self.parser_stacktrace.pop()
        return expression

    def term_expression(self) -> Expression:
        self.parser_stacktrace.append("term_expression")
        expression = self.factor_expression()

        while self.look(TokenType.PLUS, TokenType.MINUS):
            op_token = self.get()
            if self.match(TokenType.PLUS):
                expression = BinaryExpression(expression, self.factor_expression(), '+', op_token)
                continue
            if self.match(TokenType.MINUS):
                expression = BinaryExpression(expression, self.factor_expression(), '-', op_token)
                continue
            break

        self.parser_stacktrace.pop()
        return expression

    def factor_expression(self) -> Expression:
        self.parser_stacktrace.append("factor_expression")
        expression = self.unary_expression()

        operators = (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO)

        while self.look(*operators):
            op_token = self.get()
            if self.match(*operators):
                expression = BinaryExpression(expression, self.unary_expression(), op_token.value, op_token)
                continue
            break

        self.parser_stacktrace.pop()
        return expression

    def unary_expression(self) -> Expression:
        self.parser_stacktrace.append("unary_expression")

        token = self.get()

        operators = (TokenType.PLUS, TokenType.MINUS)

        if self.match(*operators):
            return UnaryExpression(self.primary_expression(), token.value, token)

        self.parser_stacktrace.pop()
        return self.primary_expression()

    def primary_expression(self) -> Expression:
        self.parser_stacktrace.append("primary_expression")
        token = self.get()

        self.expect(TokenType.NUMBER, TokenType.LPAREN)

        try:
            if token.type == TokenType.NUMBER:
                if '.' in token.value: return FloatExpression(float(token.value), token)
                return IntExpression(int(token.value), token)
            elif token.type == TokenType.LPAREN:
                expression = self.expression()
                self.expect(TokenType.RPAREN)
                return expression
        finally:
            self.parser_stacktrace.pop()
