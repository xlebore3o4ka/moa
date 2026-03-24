from array import array

from vm import Specification
from vm.VMRuntimeError import VMRuntimeError


class Stack:
    def __init__(self, spec: Specification):
        self.spec = spec
        self._size = 256
        self._data = array(self.spec.TYPECODE, [0] * self._size)
        self._top = 0

    def push(self, value: int):
        if value > self.spec.BITNESS_MASK:
            raise VMRuntimeError(VMRuntimeError.Type.ARITHMETIC_OVERFLOW,
                                 f"Value {value} exceeds {self.spec.BITNESS}-bit limit")
        if value < 0:
            raise VMRuntimeError(VMRuntimeError.Type.ARITHMETIC_UNDERFLOW,
                                 f"Negative value {value} in unsigned context")

        if self._top >= self._size:
            self._data.extend([0] * self._size)
            self._size *= 2

        self._data[self._top] = value
        self._top += 1

    def pop(self) -> int:
        self._top -= 1
        if self._top < 0:
            raise VMRuntimeError(VMRuntimeError.Type.STACK_UNDERFLOW)
        return self._data[self._top]

    def peek(self) -> int:
        return self._data[self._top - 1]

    def snapshot(self):
        stack = Stack(self.spec)
        stack._data = array(self.spec.TYPECODE, self._data)
        stack._top = self._top
        stack._size = self._size
        return stack

    def __iter__(self):
        return iter(self._data[:self._top])
