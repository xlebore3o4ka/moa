from compiler.AST.Expression import Expression
from compiler.Token import Token
from vm.codegen import Codegen


class FloatExpression(Expression):
    def __init__(self, value: float, token: Token):
        super().__init__(token)
        self.value = value

    def compile(self) -> Codegen:
        from compiler.type.Types import Types
        self.return_type = Types.Float
        return Codegen().FLOAT_PUSH(self.value)

    def accept(self, visitor):
        return visitor.visit_FloatExpression(self)
