from compiler.AST.Expression import Expression
from compiler.Errors import CompilerError, Error
from compiler.Token import Token
from compiler.type.Types import Types
from vm.codegen import Codegen


class BinaryExpression(Expression):
    def __init__(self, expr1: Expression, expr2: Expression, op: str, op_token: Token):
        super().__init__(op_token)
        self.expr1 = expr1
        self.expr2 = expr2
        self.op = op

    def compile(self) -> Codegen:
        codegen = Codegen()

        expr_codegen1 = self.expr1.compile()
        expr_codegen2 = self.expr2.compile()
        try:
            if self.expr1.return_type in [Types.Int, Types.Float] and self.expr2.return_type in [Types.Int, Types.Float]:
                self.return_type = Types.Int if self.expr1.return_type == self.expr2.return_type == Types.Int else Types.Float

                if (self.expr1.return_type == Types.Int and self.expr2.return_type == Types.Float or
                        self.op == '/' and self.expr1.return_type == Types.Int):
                    expr_codegen1.INT_FLOAT()
                if (self.expr2.return_type == Types.Int and self.expr1.return_type == Types.Float or
                        self.op == '/' and self.expr2.return_type == Types.Int):
                    expr_codegen2.INT_FLOAT()

                codegen.extend(expr_codegen1.extend(expr_codegen2))

                if self.op == '/' and Error.DEBUG:
                    codegen.ERROR_DATA("ZeroDivisionError", self.token.line, self.token.col, self.token.length,
                                       self.token.lexeme, self.token.file)

                {
                    '+': [codegen.INT_ADD, codegen.FLOAT_ADD],
                    '-': [codegen.INT_SUB, codegen.FLOAT_SUB],
                    '*': [codegen.INT_MUL, codegen.FLOAT_MUL],
                    '/': [codegen.FLOAT_DIV, codegen.FLOAT_DIV],
                    '%': [codegen.INT_MOD]
                }[self.op][0 if self.return_type == Types.Int else 1]()
        except (KeyError, IndexError):
            raise CompilerError.from_token(
                "TypeMismatchError",
                f"Invalid binary operation '{self.op}' for types {self.expr1.return_type} and {self.expr2.return_type}",
                self.token,
                "BinaryExpression"
            )

        return codegen

    def accept(self, visitor):
        return visitor.visit_BinaryExpression(self)
