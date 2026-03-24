from array import array

from vm import Specification
from vm.VMRuntimeError import VMRuntimeError


class Memory:
    def __init__(self, spec: Specification):
        self.spec = spec
        self._size = 256
        self._data = array(self.spec.TYPECODE, [0] * self._size)

    def _ensure_capacity(self, address: int):
        if address >= self._size:
            new_size = self._size
            while address >= new_size:
                new_size *= 2
            self._data.extend([0] * (new_size - self._size))
            self._size = new_size

    def load(self, address: int) -> int:
        if address < 0:
            raise VMRuntimeError(VMRuntimeError.Type.MEMORY_ACCESS_VIOLATION,
                                 f"Negative memory address {address}")
        if address >= self._size:
            return 0
        return self._data[address]

    def store(self, address: int, value: int):
        if value > self.spec.BITNESS_MASK:
            raise VMRuntimeError(VMRuntimeError.Type.ARITHMETIC_OVERFLOW,
                                 f"Value {value} exceeds {self.spec.BITNESS}-bit limit")
        if value < 0:
            raise VMRuntimeError(VMRuntimeError.Type.ARITHMETIC_UNDERFLOW,
                                 f"Negative value {value} in unsigned context")
        if address < 0:
            raise VMRuntimeError(VMRuntimeError.Type.MEMORY_ACCESS_VIOLATION,
                                 f"Negative memory address {address}")

        self._ensure_capacity(address)
        self._data[address] = value

    def snapshot(self):
        memory = Memory(self.spec)
        memory._data = array(self.spec.TYPECODE, self._data)
        memory._size = self._size
        return memory

    def __getitem__(self, address: int) -> int:
        return self.load(address)

    def __setitem__(self, address: int, value: int):
        self.store(address, value)