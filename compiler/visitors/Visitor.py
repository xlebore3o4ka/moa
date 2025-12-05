from abc import abstractmethod, ABC

from compiler.AST.BinaryExpression import BinaryExpression
from compiler.AST.FloatExpression import FloatExpression
from compiler.AST.IntExpression import IntExpression


class Visitor(ABC):
    @abstractmethod
    def visit_FloatExpression(self, float_expression: FloatExpression): pass

    @abstractmethod
    def visit_IntExpression(self, integer_expression: IntExpression): pass

    @abstractmethod
    def visit_BinaryExpression(self, binary_expression: BinaryExpression): pass

    @abstractmethod
    def visit_UnaryExpression(self, unary_expression: BinaryExpression): pass
