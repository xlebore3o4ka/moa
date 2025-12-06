from compiler.Errors import Error
from compiler.Lexer import Lexer
from compiler.Parser import Parser
from compiler.visitors.DebugVisitor import DebugVisitor
from vm.codegen import Codegen

print("source code --->\n")

print(text := """4 * (10 + (4 - 5)) / 2.5""")

print("\ntokenizing --->\n")

try:
    Error.DEBUG = True

    lexer = Lexer(text, filename:="test.moa")
    tokens = lexer.tokenize()

    for token in tokens:
        print(f"at {token.line}:{token.col} {token}")

    print("\nparsing --->\n")

    parser = Parser(tokens, filename)
    expression = parser.parse()  # TODO: BlockStatement

    debug_visitor = DebugVisitor()
    print(expression.accept(debug_visitor))

    print("\ncompiling --->\n")

    codegen = expression.compile()
    print('[', ', '.join(map(lambda b: f"0x{b:02x}", list(codegen.build()))), ']')

    print("\ndissassembling --->\n")
    print(codegen.disassemble())

except Error as e:
    pass
