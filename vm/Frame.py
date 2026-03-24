from typing import Optional

from vm.Stack import Stack
from vm.Specification import Specification


class Frame:
    def __init__(self, spec: Specification, name: str, call: int, ret: int):
        self.spec = spec
        self.name = name
        self.stack = Stack(self.spec)
        self.prev: Optional[Frame] = None
        self.call = call
        self.ret = ret

    def snapshot(self):
        frame = Frame(self.spec, self.name, self.call, self.ret)
        frame.stack = self.stack.snapshot()
        frame.prev = self.prev.snapshot() if self.prev else None
        frame.ret = self.ret
        return frame