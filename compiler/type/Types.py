from compiler.AST.FloatExpression import FloatExpression
from compiler.AST.IntExpression import IntExpression
from compiler.type.Type import Type


class Types:
    Int = Type("Int", IntExpression)
    Float = Type("Float", FloatExpression)