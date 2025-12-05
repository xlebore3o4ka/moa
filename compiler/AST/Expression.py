from abc import ABC, abstractmethod
from typing import Optional

from compiler.AST.Node import Node
from compiler.Token import Token
from compiler.type.Type import Type
from vm.codegen import Codegen


class Expression(Node):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.return_type: Optional[Type] = None

    @abstractmethod
    def compile(self) -> Codegen:
        pass

    @abstractmethod
    def accept(self, visitor):
        pass
