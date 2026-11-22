
import argparse
import io
import os
import tempfile
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from pprint import pprint

from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer, SemanticError
from src.ir import IRGenerator, print_ir
from src.llvm_backend import LLVMBackend


VERSION = "0.1.0"


def print_source_diagnostic(category, input_path, error):
    import re

    message = str(error)
    match = re.search(r"at line (\d+), column (\d+)", message)
    line = int(match.group(1)) if match else 1
    column = int(match.group(2)) if match else 1

    explanation = re.sub(
        r" at line \d+, column \d+",
        "",
        message
    )
    explanation = re.sub(
        r"^UNSUPPORTED_PREPROCESSING_DIRECTIVE: ",
        "",
        explanation
    )
    explanation = re.sub(
        r"^UNSUPPORTED_LINE_SPLICING: ",
        "",
        explanation
    )

    print(
        f"ERROR {category} {input_path}:{line}:{column}: "
        f"{explanation}",
        file=sys.stderr
    )


def compile_lexer(source):
    """Convert source code into tokens."""
    return Lexer(source).tokenize()


def compile_parser(tokens):
    """Convert tokens into an abstract syntax tree."""
    return Parser(tokens).parse()


def compile_semantics(ast):
    """Perform semantic analysis."""
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer


def generate_student_ir(ast):
    """Generate the student's intermediate representation."""
    return IRGenerator().generate(ast)


def generate_llvm_ir(ir):
    """Convert student IR into LLVM IR."""
    return LLVMBackend().generate(ir)


def format_student_ir(ir):
    """Capture the output of the IR printer."""
    output = io.StringIO()

    with redirect_stdout(output):
        result = print_ir(ir)

    if result is not None:
        return str(result)

    return output.getvalue()


def show_capabilities():
    print("C Minor Compiler")
    print("Version:", VERSION)
    print("Target: x86_64-pc-linux-gnu")

    try:
        result = subprocess.run(
            ["llc", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        llvm_version = result.stdout.splitlines()[0]
    except (FileNotFoundError, subprocess.CalledProcessError):
        llvm_version = "LLVM toolchain unavailable"

    print("LLVM toolchain:", llvm_version)
    print()
    print("Available components:")
    print("- Lexer")
    print("- Parser and AST")
    print("- Semantic Analyzer")
    print("- Symbol Table")
    print("- Student Intermediate Representation")
    print("- LLVM Backend")
    print()
    print("Supported backend: LLVM")
    print("QBE backend: Not implemented")
    print()
    print("Accepted source form: One self-contained C Minor source file")
    print("Preprocessing: Disabled")
    print("Preprocessor directives and line splicing: Rejected")
    print()
    print("Minimum tested input capacities:")
    print("- Source size: 32 KiB")
    print("- Tokens: 4,000")
    print("- Block nesting: 16 levels")
    print("- Expression nesting: 16 levels")
    print("- Function definitions: 32")
    print("- Parameters per function: 6")
    print("- Local declarations per block: 64")
    print("- Source line length: 2,048 characters")


def create_argument_parser():
    parser = argparse.ArgumentParser(
        prog="cminorcc",
        description="C Minor Compiler"
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Input C Minor source file"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output assembly filename"
    )

    parser.add_argument(
        "--backend",
        choices=["llvm", "qbe"],
        default="llvm",
        help="Select compiler backend (default: llvm)"
    )

    actions = parser.add_mutually_exclusive_group()

    actions.add_argument(
        "--check",
        action="store_true",
        help="Check the source without generating assembly"
    )

    actions.add_argument(
        "--dump-tokens",
        action="store_true",
        help="Display lexer tokens"
    )

    actions.add_argument(
        "--dump-ast",
        action="store_true",
        help="Display the abstract syntax tree"
    )

    actions.add_argument(
        "--dump-symbols",
        action="store_true",
        help="Display function symbol information"
    )

    actions.add_argument(
        "--dump-ir",
        action="store_true",
        help="Display student intermediate representation"
    )

    actions.add_argument(
        "--emit-backend-ir",
        action="store_true",
        help="Display generated LLVM IR"
    )

    actions.add_argument(
        "--capabilities",
        action="store_true",
        help="Display compiler capabilities"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )

    return parser


def main():
    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    if args.capabilities:
        show_capabilities()
        return 0

    if not args.input:
        argument_parser.error("an input source file is required")

    if args.backend == "qbe":
        print(
            "Error: QBE backend is not implemented.",
            file=sys.stderr
        )
        return 1

    input_path = Path(args.input)

    if input_path.suffix.lower() not in {".cm", ".c"}:
        print(
            f"Error: Unsupported source file extension: "
            f"{input_path.suffix}. Use .cm or .c.",
            file=sys.stderr
        )
        return 1

    if not input_path.is_file():
        print(
            f"Error: Input file not found: {input_path}",
            file=sys.stderr
        )
        return 1

    try:
        # Enforce the SRS source-size limit before reading the file.
        source_size = input_path.stat().st_size

        if source_size > 32 * 1024:
            print(
                "ERROR RESOURCE_LIMIT "
                f"{input_path}:1:1: "
                "Source file exceeds the maximum size of 32 KiB.",
                file=sys.stderr
            )
            return 1

        # Stage 1: Read source code.
        source = input_path.read_text(encoding="utf-8")

        for line_number, line in enumerate(source.splitlines(), start=1):
            if len(line) > 2048:
                print(
                    "ERROR RESOURCE_LIMIT "
                    f"{input_path}:{line_number}:2049: "
                    "Source line exceeds the maximum length of 2048 characters.",
                    file=sys.stderr
                )
                return 1

        # Stage 2: Lexical analysis.
        tokens = compile_lexer(source)

        if args.dump_tokens:
            for token in tokens:
                print(token)
            return 0

        # Stage 3: Syntax analysis and AST generation.
        ast = compile_parser(tokens)

        if args.dump_ast:
            pprint(ast)
            return 0

        # Stage 4: Semantic analysis.
        analyzer = compile_semantics(ast)

        if args.dump_symbols:
            print("FUNCTION SYMBOLS")
            print("================")

            for name, info in analyzer.functions.items():
                print(f"Function: {name}")
                print(f"  Return type: {info.return_type}")
                print(f"  Parameters: {info.parameter_types}")
                print(f"  Defined: {info.defined}")
                print()

            print("VARIABLE SCOPES")
            print("===============")

            for scope in analyzer.symbol_table.scopes:
                parent_id = (
                    scope.parent.scope_id
                    if scope.parent is not None
                    else None
                )

                print(
                    f"Scope {scope.scope_id} "
                    f"(Type: {scope.scope_type}, "
                    f"Parent: {parent_id}, "
                    f"Function: {scope.function_name})"
                )

                if not scope.symbols:
                    print("  No variables")
                else:
                    for symbol in scope.symbols.values():
                        print(
                            f"  {symbol.name}: "
                            f"{symbol.data_type} "
                            f"({symbol.symbol_type})"
                        )

                print()

            return 0

        if args.check:
            print("Semantic analysis successful.")
            return 0

        # Stage 5: Student intermediate representation.
        ir = generate_student_ir(ast)

        if args.dump_ir:
            print(format_student_ir(ir), end="")
            return 0

        # Stage 6: Backend IR generation.
        llvm_ir = generate_llvm_ir(ir)

        if args.emit_backend_ir:
            print(llvm_ir)
            return 0

        # Stage 7: Generate assembly using LLVM.
        assembly_path = (
            Path(args.output)
            if args.output
            else input_path.with_suffix(".s")
        )

        llvm_path = assembly_path.with_suffix(".ll")

        assembly_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        llvm_path.write_text(
            llvm_ir,
            encoding="utf-8"
        )

        temporary_fd, temporary_name = tempfile.mkstemp(
            prefix=f".{assembly_path.stem}_",
            suffix=".s.tmp",
            dir=str(assembly_path.parent),
        )
        os.close(temporary_fd)
        temporary_assembly = Path(temporary_name)

        try:
            subprocess.run(
                [
                    "llc",
                    "-O0",
                    "-mtriple=x86_64-pc-linux-gnu",
                    "-filetype=asm",
                    str(llvm_path),
                    "-o",
                    str(temporary_assembly)
                ],
                check=True
            )
            os.replace(temporary_assembly, assembly_path)
        finally:
            temporary_assembly.unlink(missing_ok=True)

        print("Compilation successful.")
        print(f"LLVM IR: {llvm_path}")
        print(f"Assembly: {assembly_path}")

        return 0

    except SemanticError as error:
        print_source_diagnostic(error.category, input_path, error)
        return 1

    except subprocess.CalledProcessError as error:
        print(
            f"LLVM compilation failed: {error}",
            file=sys.stderr
        )
        return 1

    except FileNotFoundError as error:
        print(
            f"Required file or tool not found: {error}",
            file=sys.stderr
        )
        return 1

    except SyntaxError as error:
        message = str(error)
        if "UNSUPPORTED_PREPROCESSING_DIRECTIVE" in message:
            category = "UNSUPPORTED_PREPROCESSING_DIRECTIVE"
        elif "UNSUPPORTED_LINE_SPLICING" in message:
            category = "UNSUPPORTED_LINE_SPLICING"
        elif "Unexpected character" in message or "Unterminated" in message:
            category = "LEXICAL_ERROR"
        else:
            category = "SYNTAX_ERROR"

        print_source_diagnostic(category, input_path, error)
        return 1

    except (ValueError, TypeError) as error:
        print(
            f"Compilation error: {error}",
            file=sys.stderr
        )
        return 1

    except Exception as error:
        print(
            f"Unexpected compilation error: {error}",
            file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
