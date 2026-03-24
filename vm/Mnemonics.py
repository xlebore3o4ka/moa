import itertools
from enum import Enum

_counter = itertools.count()


class Mnemonics(int, Enum):
    NOP = next(_counter)
    RET = next(_counter)
    CALL = next(_counter)

    PUSH = next(_counter)
    POP = next(_counter)

    ADD = next(_counter)
    SUB = next(_counter)
    MUL = next(_counter)
    UDIV = next(_counter)
    UMOD = next(_counter)

    EQ = next(_counter)
    NEQ = next(_counter)
    ULT = next(_counter)
    ULTE = next(_counter)
    UGT = next(_counter)
    UGTE = next(_counter)

    CAND = next(_counter)
    COR = next(_counter)
    CNOT = next(_counter)

    JMP = next(_counter)
    JZ = next(_counter)
    JNZ = next(_counter)

    STG = next(_counter)
    LDG = next(_counter)

    @staticmethod
    def from_opcode(opcode: int):
        for mnemonic in Mnemonics:
            if mnemonic.value == opcode:
                return mnemonic
        return None
