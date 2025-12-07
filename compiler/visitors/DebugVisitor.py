from compiler.AST.BinaryExpression import BinaryExpression
from compiler.AST.FloatExpression import FloatExpression
from compiler.AST.IntExpression import IntExpression
from compiler.AST.UnaryExpression import UnaryExpression
from compiler.visitors.Visitor import Visitor
import json
from typing import Dict, Any


class DebugVisitor(Visitor):
    def __init__(self):
        self.indent = 0

    def visit_UnaryExpression(self, unary_expression: UnaryExpression) -> Dict[str, Any]:
        return {
            "type": "UnaryExpression",
            "op": unary_expression.op,
            "expr": unary_expression.expr.accept(self)
        }

    def visit_BinaryExpression(self, binary_expression: BinaryExpression) -> Dict[str, Any]:
        return {
            "type": "BinaryExpression",
            "op": binary_expression.op,
            "left": binary_expression.expr1.accept(self),
            "right": binary_expression.expr2.accept(self)
        }

    def visit_FloatExpression(self, float_expression: FloatExpression) -> Dict[str, Any]:
        return {
            "type": "FloatExpression",
            "value": float_expression.value
        }

    def visit_IntExpression(self, integer_expression: IntExpression) -> Dict[str, Any]:
        return {
            "type": "IntExpression",
            "value": integer_expression.value
        }

    @staticmethod
    def pretty_print(ast_data: Dict[str, Any]) -> str:
        print(pretty_str:=json.dumps(ast_data, indent=2, ensure_ascii=False))
        return pretty_str