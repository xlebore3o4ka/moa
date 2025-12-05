class Codegen:
    def __init__(self):
        self.bytecode = bytearray()

    def _b(self, b):
        self.bytecode.append(b & 0xFF)

    def _i64(self, v):
        self.bytecode.extend(v.to_bytes(8, 'little', signed=True))

    def _f64(self, v):
        import struct
        self.bytecode.extend(struct.pack('<d', v))

    def extend(self, codegen: 'Codegen'):
        self.bytecode.extend(codegen.bytecode)
        return self

    def NOP(self):
        self._b(0x00)
        return self

    def INT_PUSH(self, v):
        self._b(0x01)
        self._i64(v)
        return self

    def INT_ADD(self):
        self._b(0x02)
        return self

    def INT_SUB(self):
        self._b(0x03)
        return self

    def INT_MUL(self):
        self._b(0x04)
        return self

    def INT_DIV(self):
        self._b(0x05)
        return self

    def INT_MOD(self):
        self._b(0x06)
        return self

    def INT_NEG(self):
        self._b(0x07)
        return self

    def INT_FLOAT(self):
        self._b(0x08)
        return self

    def FLOAT_PUSH(self, v):
        self._b(0x09)
        self._f64(v)
        return self

    def FLOAT_ADD(self):
        self._b(0x0a)
        return self

    def FLOAT_SUB(self):
        self._b(0x0b)
        return self

    def FLOAT_MUL(self):
        self._b(0x0c)
        return self

    def FLOAT_DIV(self):
        self._b(0x0d)
        return self

    def FLOAT_NEG(self):
        self._b(0x0e)
        return self

    def FLOAT_INT(self):
        self._b(0x0f)
        return self

    def build(self):
        return bytes(self.bytecode)
