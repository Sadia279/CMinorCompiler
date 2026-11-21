# C Minor Compiler

## 1. Project Overview

C Minor Compiler is a student-developed compiler for a course-defined subset of the C programming language. It translates C Minor source code through a student-developed compiler pipeline into LLVM Intermediate Representation (LLVM IR), then generates x86-64 assembly.

The project is implemented in Python and targets Linux x86-64.

## 2. Technologies and Tools

| Component | Technology |
|---|---|
| Implementation language | Python 3 |
| Lexer | Student-developed Python implementation |
| Parser | Student-developed recursive descent parser |
| Syntax representation | Abstract Syntax Tree (AST) |
| Semantic analysis | Student-developed |
| Intermediate representation | Student-developed three-address-code-style IR |
| Backend | LLVM 21.1.8 |
| Assembly generation | LLVM `llc` |
| Assembler and linker | GCC |
| Target architecture | x86-64 Linux |

## 3. Compiler Architecture

The compiler processes source programs through these stages:

1. **Source input:** Reads a self-contained `.cm` source file.
2. **Lexical analysis:** Converts source characters into tokens.
3. **Syntax analysis:** Parses tokens and constructs an AST.
4. **Semantic analysis:** Checks declarations, scopes, types, and function usage.
5. **Student IR generation:** Produces the compiler's own intermediate representation.
6. **LLVM IR generation:** Converts the student IR into LLVM IR.
7. **Assembly generation:** Invokes LLVM `llc` to generate x86-64 assembly.
8. **Native build:** GCC can assemble and link the generated assembly into an executable.

The compiler's lexer, parser, semantic analyzer, and student IR are implemented as part of this project.

## 4. Project Structure

```text
CMinorCompiler/
├── src/
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic.py
│   ├── ir.py
│   ├── llvm_backend.py
│   └── main.py
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_ir.py
│   ├── test_llvm_backend.py
│   ├── test_fuzz.py
│   └── test_end_to_end.py
├── examples/
├── requirements.txt
└── README.md
```

## 5. Requirements and Setup

Required tools:

- Python 3
- LLVM, including `llc`
- GCC

On Ubuntu, install the system dependencies:

```bash
sudo apt update
sudo apt install python3 python3-venv llvm gcc
```

Create and activate a virtual environment:

```bash
cd ~/CMinorCompiler
python3 -m venv venv
source venv/bin/activate
```

No third-party Python packages are required. The compiler uses the system-installed LLVM `llc` and GCC tools.

Check compiler capabilities:

```bash
python -m src.main --capabilities
```

## 6. Compiling a Program

Compile an example:

```bash
python -m src.main examples/cli_test.cm
```

Specify an assembly output path:

```bash
python -m src.main examples/cli_test.cm -o output/program.s
```

Build and run an executable:

```bash
gcc -no-pie output/program.s -o output/program
./output/program
echo $?
```

## 7. Command-Line Options

| Option | Description |
|---|---|
| `--help` | Displays command-line help |
| `--version` | Displays compiler version |
| `--capabilities` | Displays compiler and toolchain capabilities |
| `--check` | Performs compilation checks |
| `--dump-tokens` | Displays lexical tokens |
| `--dump-ast` | Displays the Abstract Syntax Tree |
| `--dump-symbols` | Displays symbol information |
| `--dump-ir` | Displays student-developed intermediate representation |
| `--emit-backend-ir` | Displays generated backend LLVM IR |
| `--backend=llvm` | Selects the implemented LLVM backend |
| `--backend=qbe` | Selects QBE; currently unsupported |
| `-o PATH` | Specifies the assembly output path |

Examples:

```bash
python -m src.main examples/cli_test.cm --dump-tokens
python -m src.main examples/cli_test.cm --dump-ast
python -m src.main examples/cli_test.cm --dump-symbols
python -m src.main examples/cli_test.cm --dump-ir
python -m src.main examples/cli_test.cm --emit-backend-ir
python -m src.main examples/cli_test.cm --check
```

## 8. Supported Language Features

- Integer and void functions
- Function declarations and definitions
- Function parameters and function calls
- Local integer variables
- Arithmetic operators: `+`, `-`, `*`, `/`, `%`
- Relational and equality operators
- Logical operators: `!`, `&&`, `||`
- Assignment statements and supported assignment expressions
- `if` and `else` statements
- `while` and `for` loops
- `break` and `continue`
- Nested blocks and variable scopes
- Recursive function calls

Only constructs supported by the implemented C Minor grammar should be used.

## 9. Source Input Restrictions

Each compilation accepts one self-contained C Minor source file.

The compiler does not run a C preprocessor. Preprocessor directives such as `#include` and `#define` are rejected. Backslash-newline line splicing is also rejected.

Directive-like text inside comments is treated as comment content.

The compiler supports only the defined C Minor language subset, not the full C language.

## 10. Tested Input Boundaries

The following minimum input capacities have been tested:

| Input characteristic | Tested capacity |
|---|---:|
| Source file size | 32 KiB |
| Tokens | 4,000 |
| Nested blocks | 16 levels |
| Nested expressions | 16 levels |
| Function definitions | 32 |
| Parameters per function | 6 |
| Local declarations in one block | 64 |
| Source line length | 2,048 characters |

These values describe tested boundaries, not a guarantee that every larger input is supported.

## 11. Running Automated Tests

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

Latest verified result:

```text
Ran 109 tests
OK
```

The suite includes lexer, parser, semantic analysis, IR, LLVM backend, malformed-input robustness, and end-to-end execution tests.

The end-to-end tests compile example programs, assemble and link generated assembly with GCC, execute the programs, and check their exit statuses. A runtime test also checks logical-operator short-circuit behavior.

## 12. Exit Status and Diagnostics

| Exit status | Meaning |
|---|---|
| `0` | Successful operation |
| `1` | Compilation, input, file, unsupported-feature, or backend failure |
| `2` | Command-line argument error |

Diagnostics are written to standard error. Stage dumps and requested backend IR are written to standard output.

## 13. Compiler Information

- Compiler name: C Minor Compiler
- Version: 0.1.0
- Implementation: Python
- Backend: LLVM
- LLVM version in the development environment: 21.1.8
- Target: x86-64 Linux
- Project type: Academic compiler development

Use `python -m src.main --capabilities` to inspect the current environment's capabilities.

## 14. Current Limitations

- Only the defined C Minor language subset is supported.
- QBE backend support is not implemented.
- Preprocessing is disabled.
- The compiler targets x86-64 Linux.
- The installed LLVM version may differ in another environment.
