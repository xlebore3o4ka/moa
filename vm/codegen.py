import struct
from dataclasses import dataclass


class Instructions:
    opcode_map = {}


def _inst(opcode):
    def _decorator(func):
        def wrapper(self, *args, **kwargs):
            self._b(opcode)
            return func(self, *args, **kwargs)

        Instructions.opcode_map[func.__name__] = opcode
        wrapper.__name__ = func.__name__

        return wrapper

    return _decorator


class Codegen:
    def __init__(self):
        self.bytecode = bytearray()
        self._opcode_map = Instructions.opcode_map

    def disassemble(self):
        output = []

        reverse_opcode_map = {v: k for k, v in self._opcode_map.items()}

        max_opcode_name_len = max(len(k) for k in reverse_opcode_map.values())
        max_value_len = 0

        @dataclass
        class ToDisasmInstruction:
            address: int
            opcode: int
            value: str
            bytes: bytes

        to_disasm_instructions = []

        i = 0
        while i < len(self.bytecode):
            address = i
            opcode = self.bytecode[i]
            i += 1
            if opcode == self.opcode(self.INT_PUSH):
                arguments = self.bytecode[i:i+8]
                i += 8
                value = str(int.from_bytes(arguments, 'little', signed=True))
                max_value_len = max(max_value_len, len(value))
                to_disasm_instructions.append(ToDisasmInstruction(address, opcode, value, arguments))
            elif opcode == self.opcode(self.FLOAT_PUSH):
                arguments = self.bytecode[i:i+8]
                i += 8
                value = str(struct.unpack('<d', arguments)[0])
                max_value_len = max(max_value_len, len(value))
                to_disasm_instructions.append(ToDisasmInstruction(address, opcode, value, arguments))
            else:
                to_disasm_instructions.append(ToDisasmInstruction(address, opcode, '', b''))

        for inst in to_disasm_instructions:
            print(f"[{inst.address:08x}] {reverse_opcode_map[inst.opcode]:{max_opcode_name_len}s}  "
                  f"{inst.value:{max_value_len}s}  ; {' '.join(map(lambda b: f"{b:02x}", inst.bytes))}")

        return '\n'.join(output)

    def _b(self, b):
        self.bytecode.append(b & 0xFF)
        return self

    def _i64(self, v):
        self.bytecode.extend(v.to_bytes(8, 'little', signed=True))
        return self

    def _f64(self, v):
        import struct
        self.bytecode.extend(struct.pack('<d', v))
        return self

    def opcode(self, instruction) -> int:
        return self._opcode_map.get(instruction.__name__)

    def extend(self, codegen: 'Codegen'):
        self.bytecode.extend(codegen.bytecode)
        return self

    @_inst(0x00)
    def NOP(self):
        return self

    @_inst(0x01)
    def INT_PUSH(self, v):
        return self._i64(v)

    @_inst(0x02)
    def INT_ADD(self):
        return self

    @_inst(0x03)
    def INT_SUB(self):
        return self

    @_inst(0x04)
    def INT_MUL(self):
        return self

    @_inst(0x05)
    def INT_DIV(self):
        return self

    @_inst(0x06)
    def INT_MOD(self):
        return self

    @_inst(0x07)
    def INT_NEG(self):
        return self

    @_inst(0x08)
    def INT_FLOAT(self):
        return self

    @_inst(0x09)
    def FLOAT_PUSH(self, v):
        return self._f64(v)

    @_inst(0x0a)
    def FLOAT_ADD(self):
        return self

    @_inst(0x0b)
    def FLOAT_SUB(self):
        return self

    @_inst(0x0c)
    def FLOAT_MUL(self):
        return self

    @_inst(0x0d)
    def FLOAT_DIV(self):
        return self

    @_inst(0x0e)
    def FLOAT_NEG(self):
        return self

    @_inst(0x0f)
    def FLOAT_INT(self):
        return self

    def build(self):
        return bytes(self.bytecode)
