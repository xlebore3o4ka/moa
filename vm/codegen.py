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

    @property
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
                arguments = self.bytecode[address:i + 8]
                i += 8
                value = str(int.from_bytes(arguments[1:], 'little', signed=True))
                max_value_len = max(max_value_len, len(value))
                to_disasm_instructions.append(ToDisasmInstruction(address, opcode, value, arguments))
            elif opcode == self.opcode(self.FLOAT_PUSH):
                arguments = self.bytecode[address:i + 8]
                i += 8
                value = str(struct.unpack('<d', arguments[1:])[0])
                max_value_len = max(max_value_len, len(value))
                to_disasm_instructions.append(ToDisasmInstruction(address, opcode, value, arguments))
            elif opcode == self.opcode(self.ERROR_DATA):
                # Читаем длину type
                type_len = self.bytecode[i]
                i += 1

                # Читаем type
                type_str = self.bytecode[i:i + type_len].decode()
                i += type_len

                # Читаем line (u32)
                line = int.from_bytes(self.bytecode[i:i + 4], 'little')
                i += 4

                # Читаем column (u16)
                column = int.from_bytes(self.bytecode[i:i + 2], 'little')
                i += 2

                # Читаем length (u16)
                length = int.from_bytes(self.bytecode[i:i + 2], 'little')
                i += 2

                # Читаем длину lexeme (u16)
                lexeme_len = int.from_bytes(self.bytecode[i:i + 2], 'little')
                i += 2

                # Читаем lexeme
                lexeme = self.bytecode[i:i + lexeme_len].decode()
                i += lexeme_len

                # Читаем длину file (u16)
                file_len = int.from_bytes(self.bytecode[i:i + 2], 'little')
                i += 2

                # Читаем file
                file = self.bytecode[i:i + file_len].decode()
                i += file_len

                # Формируем значение для отображения
                arguments = self.bytecode[address:i]
                value = type_str
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

    def _u32(self, v):
        self.bytecode.extend(v.to_bytes(4, 'little', signed=False))
        return self

    def _u16(self, v):
        self.bytecode.extend(v.to_bytes(2, 'little', signed=False))
        return self

    def _u8(self, v):
        self.bytecode.append(v & 0xFF)
        return self

    def _utf8(self, s):
        encoded = s.encode('utf-8')
        self.bytecode.extend(encoded)
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

    @_inst(0x10)
    def ERROR_DATA(self, type: str, line: int, column: int, length: int, lexeme: str, file: str):
        return (self._u8(len(type))._utf8(type)._u32(line)._u16(column)._u16(length)
                ._u16(len(lexeme))._utf8(lexeme)._u16(len(file))._utf8(file))

    def build(self):
        return bytes(self.bytecode)
