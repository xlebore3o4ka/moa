from abc import ABC, abstractmethod

from compiler.Token import Token
from vm.codegen import Codegen


class Node(ABC):
    def __init__(self, token: Token) -> None:
        self.token = token

    @abstractmethod
    def compile(self) -> Codegen: pass

    @abstractmethod
    def accept(self, visitor): pass
