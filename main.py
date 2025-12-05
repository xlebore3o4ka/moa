from compiler.Lexer import Lexer
from compiler.Parser import Parser
from compiler.visitors.DebugVisitor import DebugVisitor
from vm.codegen import Codegen

print("source code --->\n")

print(text := """10 * (2 + 10.0) % -2""")

print("\ntokenizing --->\n")

try:

    lexer = Lexer(text, "test.moa")
    tokens = lexer.tokenize()

    for token in tokens:
        print(f"at {token.line}:{token.col} {token}")

    print("\nparsing --->\n")

    parser = Parser(tokens)
    expression = parser.parse()  # TODO: BlockStatement

    debug_visitor = DebugVisitor()
    print(expression.accept(debug_visitor))

    print("\ncompiling --->\n")

    codegen = Codegen()
    print([*expression.compile().build()])

except Exception as e:
    pass
