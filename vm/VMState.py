from __future__ import annotations

from vm.Frame import Frame
from vm.Memory import Memory
from vm.SourceMap import SourceMap
from vm.Specification import Specification


class VMState:
    def __init__(self, specification: Specification, program: bytearray, sourcemap: SourceMap,
                 framename_pool: dict[int, str]):
        self.spec = specification
        self.pc = 0
        self.running = True
        self.program = program
        self.sourcemap = sourcemap
        self.framename_pool = framename_pool  # {frame_address: name}
        self.frame = Frame(self.spec, self.framename_pool[0], 0, 0)
        self.globals = Memory(self.spec)

    def snapshot(self) -> VMState:
        state = VMState(self.spec, self.program, self.sourcemap, self.framename_pool)  # sourcemap & program never changes
        state.pc = self.pc
        state.running = self.running
        state.frame = self.frame.snapshot()
        state.globals = self.globals.snapshot()
        return state
