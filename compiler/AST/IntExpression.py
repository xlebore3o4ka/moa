from compiler.AST.Expression import Expression
from compiler.Token import Token
from vm.codegen import Codegen


class IntExpression(Expression):
    def __init__(self, value: int, token: Token):
        super().__init__(token)
        self.value = value

    def compile(self) -> Codegen:
        from compiler.type.Types import Types
        self.return_type = Types.Int
        return Codegen().INT_PUSH(self.value)

    def accept(self, visitor):
        return visitor.visit_IntExpression(self)
