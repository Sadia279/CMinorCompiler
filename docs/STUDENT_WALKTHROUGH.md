# C Minor Compiler — Student Walkthrough

## 1. Project Purpose

This project implements a compiler for a restricted C Minor language.
It translates a source `.cm` file into x86-64 assembly using the
project's own compiler stages and an LLVM backend.

## 2. Compilation Pipeline

1. Lexer (`src/lexer.py`): Reads source code and produces tokens.
2. Parser (`src/parser.py`): Parses tokens and constructs an AST.
3. Semantic Analyzer (`src/semantic.py`): Checks declarations, scopes,
   types, and function usage.
4. Student IR Generator (`src/ir.py`): Produces the project's own
   intermediate representation.
5. LLVM Backend (`src/llvm_backend.py`): Converts project IR into LLVM IR.
6. Compiler Driver (`src/main.py`): Invokes LLVM `llc` to generate assembly.
7. Native Build: GCC assembles and links the generated assembly.

## 3. Build and Run

From the project root:

    venv/bin/python -m src.main --capabilities
    venv/bin/python -m src.main examples/cli_test.cm -o output.s
    gcc -c output.s -o output.o
    gcc -no-pie output.o -o output
    ./output

The expected exit status of `cli_test.cm` is 30.

## 4. Inspect Compiler Stages

    venv/bin/python -m src.main examples/cli_test.cm --dump-tokens
    venv/bin/python -m src.main examples/cli_test.cm --dump-ast
    venv/bin/python -m src.main examples/cli_test.cm --dump-symbols
    venv/bin/python -m src.main examples/cli_test.cm --dump-ir
    venv/bin/python -m src.main examples/cli_test.cm --emit-backend-ir
    venv/bin/python -m src.main examples/cli_test.cm --check

These options allow inspection of the compiler's intermediate stages.

## 5. Run Automated Tests

Run the full test suite:

    venv/bin/python -m unittest discover -s tests -v

Run the malformed-input test separately:

    venv/bin/python -m unittest tests.test_fuzz -v

The recorded full test suite contains 109 passing test methods.
The malformed-input test exercises 100 distinct generated inputs.
See `docs/evidence/` for the recorded test outputs.

## 6. Important Limitations

- The compiler supports the documented C Minor subset, not full C.
- Preprocessor directives are rejected.
- Backslash-newline line splicing is rejected.
- LLVM is the implemented backend.
- QBE backend support is not implemented.
- The compiler targets x86-64 Linux.
- The installed LLVM version may differ in another environment.

## 7. Preparation for Evaluation

The student should be able to explain:

- The purpose of each compiler stage.
- How source code becomes tokens and an AST.
- How semantic analysis checks names, scopes, and function usage.
- Why the project has its own intermediate representation.
- How the LLVM backend generates LLVM IR.
- How `llc` generates assembly.
- How GCC assembles and links the generated assembly.
- How to run the compiler and automated tests.

The student should read and understand the implementation and verify
all commands before the evaluation.
