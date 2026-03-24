import itertools
from enum import Enum

import colorama

_counter = itertools.count()


class VMRuntimeError(Exception):
    class Type(Enum):
        ILLEGAL_INSTRUCTION = next(_counter)
        STACK_UNDERFLOW = next(_counter)
        ARITHMETIC_OVERFLOW = next(_counter)
        INVALID_PC = next(_counter)
        ZERO_DIVISION = next(_counter)
        ARITHMETIC_UNDERFLOW = next(_counter)
        MEMORY_ACCESS_VIOLATION = next(_counter)

    c0 = colorama.Fore.RESET
    c1 = colorama.Fore.RED
    c2 = colorama.Fore.MAGENTA

    def __init__(self, type: Type, message: str = ""):
        self.type = type
        self.message = message

    def print(self, state):
        from vm.VMState import VMState
        state: VMState

        c0 = "" if not state.spec.COLORED_ERROR else self.c0
        c1 = "" if not state.spec.COLORED_ERROR else self.c1
        c2 = "" if not state.spec.COLORED_ERROR else self.c2

        widths = [0, 0, 0, 0]
        lines = [[], [], [], []]
        depth = 0

        frame = state.frame
        source = state.sourcemap.get(frame.call)
        line = source.line
        col = source.col
        length = source.length

        while frame is not None:
            source = state.sourcemap.get(frame.call)
            data = [f"{source.line}:", f"{source.col}", f"\"{source.file}\"", f"{frame.name}"]

            for i, val in enumerate(data):
                lines[i].insert(0, val)
                widths[i] = max(widths[i], len(val))

            frame = frame.prev
            depth += 1

        stacktrace_splitter_val2 = "in this place: "
        widths[2] = max(widths[2], len(stacktrace_splitter_val2))

        rows = [
            "Runtime caused an ERROR from the following stacktrace:",
            f" {"p":>{widths[0]-1}}o{"s":<{widths[1]}} ┌ " + "from file".ljust(widths[2]) + f" ┌ in frame..{depth}",
        ]

        stacktrace_splitter = (f" {" ":>{widths[0]-1}}│{" ":<{widths[1]}} └ " +
                               stacktrace_splitter_val2.ljust(widths[2], '─') + "─┘")

        for i in range(len(lines[0])):
            pos = f"{lines[0][i]:>{widths[0]}}{lines[1][i]:<{widths[1]}}"
            file = f"{lines[2][i]:<{widths[2]}}"
            name = f"{lines[3][i]}"

            rows.append(f" {pos} │ {c2}{file}{c1} │ {name}")

        rows.append(stacktrace_splitter)

        lexeme_left = f" {" ":>{widths[0]-1}}└{"─":─<{widths[1]}}─>   "
        lexeme = state.sourcemap.source.split('\n')[line]
        delta_lexeme = len(lexeme) - len(lexeme.lstrip())

        rows.append(lexeme_left + c0 + lexeme.lstrip() + c1)
        rows.append("┌" + "─" * (len(lexeme_left) - 1) + "─" * (col - delta_lexeme) + "^" * length)
        if self.message:
            rows.append(f"= {c2}{self.type.name}{c1}")
            rows.append(f"└─> {c0}{self.message}{c1}")
        else:
            rows.append(f"= {c2}{self.type.name}{c1}")

        print(c1 + '\n'.join(rows) + f"{c0}\n")
