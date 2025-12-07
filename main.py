from compiler.Errors import Error
from compiler.Lexer import Lexer
from compiler.Parser import Parser

# print("source code --->\n")
#
# print(text := """(10 * 2) - 3 / 0""")
#
# print("\ntokenizing --->\n")
#
# try:
#     Error.DEBUG = True
#
#     lexer = Lexer(text, filename:="test.moa")
#     tokens = lexer.tokenize()
#
#     for token in tokens:
#         print(f"at {token.line}:{token.col} {token}")
#
#     print("\nparsing --->\n")
#
#     parser = Parser(tokens, filename)
#     expression = parser.parse()  # TODO: BlockStatement
#
#     debug_visitor = DebugVisitor()
#     DebugVisitor.pretty_print(expression.accept(debug_visitor))
#
#     print("\ncompiling --->\n")
#
#     codegen = expression.compile()
#     print('[', ', '.join(map(lambda b: f"0x{b:02x}", list(codegen.build()))), '];')
#
#     print("\ndissassembling --->\n")
#     print(codegen.disassemble)
#
# except Error as e:
#     pass
import os
import argparse


def get_tokens(source):
    with open(source, encoding="utf8") as f:
        text = f.read()
    lexer = Lexer(text, source)
    return lexer.tokenize()

def get_ast(source):
    tokens = get_tokens(source)
    parser = Parser(tokens, source)
    return parser.parse()


def get_codegen(source):
    ast = get_ast(source)
    return ast.compile()


def moa_compiler(source: str, output: str):
    codegen = get_codegen(source)
    with open(output, "wb") as f:
        f.write(codegen.build())

def main():
    parser = argparse.ArgumentParser(description='Moa Compiler')

    parser.add_argument("source", type=str, help='Path to the Moa source file')
    parser.add_argument("-o", "--output", type=str, help='Path to the output file')
    parser.add_argument("-d", "--debug", action="store_true", help='Enable debug mode')

    args = parser.parse_args()

    source = args.source
    output = args.output if args.output else f"{os.path.splitext(source)[0]}.mvm"
    Error.DEBUG = args.debug
    try:
        if not os.path.exists(args.source):
            raise Error("CompilerError", f"No such file or directory: '{args.source}'",
                        -1, -1, 0, '', args.source, "moac", ["compile"])

        moa_compiler(source, output)
    except Error as _:
        pass

if __name__ == "__main__":
    main()