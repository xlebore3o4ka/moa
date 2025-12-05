from compiler.AST.Expression import Expression
from compiler.Errors import CompilerError
from compiler.Token import Token
from compiler.type.Types import Types
from vm.codegen import Codegen


class UnaryExpression(Expression):
    def __init__(self, expr: Expression, op: str, token: Token):
        super().__init__(token)
        self.expr = expr
        self.op = op

    def compile(self) -> Codegen:
        codegen = Codegen()
        codegen.extend(self.expr.compile())

        self.return_type = self.expr.return_type

        try:
            if self.return_type in [Types.Int, Types.Float]:
                {
                    '+': [lambda: None, lambda: None],
                    '-': [codegen.INT_NEG, codegen.FLOAT_NEG]
                }[self.op][0 if self.return_type == Types.Int else 1]()
        except (KeyError, IndexError):
            raise CompilerError.from_token(
                "TypeMismatchError",
                f"Invalid unary operation '{self.op}' for type {self.expr.return_type}",
                self.token,
                "UnaryExpression"
            )

        return codegen

    def accept(self, visitor):
        return visitor.visit_UnaryExpression(self)
