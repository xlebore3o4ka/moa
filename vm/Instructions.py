from vm.Frame import Frame
from vm.Mnemonics import Mnemonics
from vm.VMRuntimeError import VMRuntimeError


def init(inst_deco):
    init_stack(inst_deco)
    init_memory(inst_deco)
    init_arithmetic(inst_deco)
    init_control_flow(inst_deco)
    init_other(inst_deco)


def init_stack(inst_deco):
    @inst_deco(Mnemonics.PUSH)
    def inst(vm):
        vm.push(vm.fetch_bitness())

    @inst_deco(Mnemonics.POP)
    def inst(vm):
        vm.pop()


def init_memory(inst_deco):
    @inst_deco(Mnemonics.STG)
    def inst(vm):
        vm.store_global(vm.fetch_bitness(), vm.pop())

    @inst_deco(Mnemonics.LDG)
    def inst(vm):
        vm.push(vm.load_global(vm.fetch_bitness()))


def init_arithmetic(inst_deco):
    def pop_a_b(vm):
        b = vm.pop()
        return vm.pop(), b

    def init_unsigned():
        @inst_deco(Mnemonics.ADD)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a + b)

        @inst_deco(Mnemonics.SUB)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a - b)

        @inst_deco(Mnemonics.MUL)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a * b)

        @inst_deco(Mnemonics.UDIV)
        def inst(vm):
            a, b = pop_a_b(vm)
            if b == 0:
                raise VMRuntimeError(VMRuntimeError.Type.ZERO_DIVISION)
            vm.push(a // b)

        @inst_deco(Mnemonics.UMOD)
        def inst(vm):
            a, b = pop_a_b(vm)
            if b == 0:
                raise VMRuntimeError(VMRuntimeError.Type.ZERO_DIVISION)
            vm.push(a % b)

        @inst_deco(Mnemonics.EQ)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a == b)

        @inst_deco(Mnemonics.NEQ)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a != b)

        @inst_deco(Mnemonics.ULT)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a < b)

        @inst_deco(Mnemonics.ULTE)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a <= b)

        @inst_deco(Mnemonics.UGT)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a > b)

        @inst_deco(Mnemonics.UGTE)
        def inst(vm):
            a, b = pop_a_b(vm)
            vm.push(a >= b)

        @inst_deco(Mnemonics.CAND)
        def inst(vm):
            false_address = vm.fetch_bitness()
            a = vm.peek()
            if a == 0:
                vm.jump(false_address)
            else:
                vm.pop()

        @inst_deco(Mnemonics.COR)
        def inst(vm):
            true_address = vm.fetch_bitness()
            a = vm.peek()
            if a != 0:
                vm.jump(true_address)
            else:
                vm.pop()

        @inst_deco(Mnemonics.CNOT)
        def inst(vm):
            vm.push(vm.pop() == 0)

    init_unsigned()


def init_control_flow(inst_deco):
    @inst_deco(Mnemonics.RET)
    def inst(vm):
        if vm.state.frame.prev is None:
            vm.state.running = False
            return
        vm.state.pc = vm.state.frame.ret
        vm.state.frame = vm.state.frame.prev

    @inst_deco(Mnemonics.CALL)
    def inst(vm):
        call_address = vm.state.pc - 1
        address = vm.fetch_bitness()
        prev = vm.state.frame
        vm.state.frame = Frame(vm.state.spec,
            name=vm.state.framename_pool[address],
            call=call_address,
            ret=vm.state.pc)
        vm.state.frame.prev = prev
        vm.jump(address)

    @inst_deco(Mnemonics.JMP)
    def inst(vm):
        vm.jump(vm.fetch_bitness())

    @inst_deco(Mnemonics.JZ)
    def inst(vm):
        address = vm.fetch_bitness()
        if vm.pop() == 0:
            vm.jump(address)

    @inst_deco(Mnemonics.JNZ)
    def inst(vm):
        address = vm.fetch_bitness()
        if vm.pop() != 0:
            vm.jump(address)


def init_other(inst_deco):
    @inst_deco(Mnemonics.NOP)
    def inst(_): ...
