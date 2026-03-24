from vm import Instructions
from vm.Mnemonics import Mnemonics
from vm.VMRuntimeError import VMRuntimeError
from vm.VMState import VMState


class VirtualMachine:
    def __init__(self, state: VMState):
        self.opcode_table = [self.illegal_instruction] * 256
        Instructions.init(self.inst_deco)
        self.state = state

    def run(self):
        try:
            while self.state.running:
                self.step()
        except IndexError:
            raise VMRuntimeError(VMRuntimeError.Type.INVALID_PC) from None
        except VMRuntimeError as e:
            e.print(self.state.snapshot())

    def step(self):
        opcode = self.fetch()
        self.opcode_table[opcode]()

    def inst_deco(self, opcode: Mnemonics):
        def wrapper(func):
            self.opcode_table[opcode.value] = lambda: func(self)
            return func

        return wrapper

    def fetch(self):
        data = self.state.program[self.state.pc]
        self.state.pc += 1
        return data

    def fetch_bitness(self):
        data = int.from_bytes(self.state.program[self.state.pc:self.state.pc + self.state.spec.BYTELENGTH],
                              self.state.spec.BYTEORDER)
        self.state.pc += self.state.spec.BYTELENGTH
        return data

    def illegal_instruction(self):
        raise VMRuntimeError(VMRuntimeError.Type.ILLEGAL_INSTRUCTION)

    def push(self, value: int):
        self.state.frame.stack.push(value)

    def pop(self):
        return self.state.frame.stack.pop()

    def peek(self):
        return self.state.frame.stack.peek()

    def jump(self, address: int):
        self.state.pc = address

    def load_global(self, index: int):
        return self.state.globals.load(index)

    def store_global(self, index: int, value: int):
        return self.state.globals.store(index, value)
