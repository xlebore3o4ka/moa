from compiler.AST.BinaryExpression import BinaryExpression
from compiler.AST.FloatExpression import FloatExpression
from compiler.AST.IntExpression import IntExpression
from compiler.AST.UnaryExpression import UnaryExpression
from compiler.visitors.Visitor import Visitor


class DebugVisitor(Visitor):
    def visit_UnaryExpression(self, unary_expression: UnaryExpression):
        return f"expr.Unary(op='{unary_expression.op}', expr={unary_expression.expr.accept(self)})"

    def visit_BinaryExpression(self, binary_expression: BinaryExpression):
        return (f"expr.Binary(expr1={binary_expression.expr1.accept(self)}, op='{binary_expression.op}', "
                f"expr2={binary_expression.expr2.accept(self)})")

    def visit_FloatExpression(self, float_expression: FloatExpression):
        return f"expr.Float(value={float_expression.value})"

    def visit_IntExpression(self, integer_expression: IntExpression):
        return f"expr.Int(value={integer_expression.value})"

    def __init__(self):
        self.indent = 0
