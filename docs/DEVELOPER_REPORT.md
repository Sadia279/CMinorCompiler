# C Minor Compiler — Developer Report

## 1. Introduction

C Minor Compiler is an academic compiler project implemented in Python. It translates a supported subset of C Minor source code into x86-64 assembly through a student-developed compiler pipeline and LLVM backend.

The main objective is to demonstrate the stages of compiler construction, from lexical analysis to native code generation.

## 2. System Architecture

The compiler consists of the following stages:

1. Lexical analysis
2. Syntax analysis and AST construction
3. Semantic analysis
4. Symbol table and scope management
5. Student-developed intermediate representation
6. LLVM IR generation
7. x86-64 assembly generation

The main entry point is `src/main.py`.

## 3. Lexical Analysis

**Source file:** `src/lexer.py`

The lexer converts source text into a sequence of tokens.

Main components:

- `Token` — represents an individual token.
- `Lexer` — processes the source program.
- `advance()` — advances through the source input.
- `tokenize()` — produces the token sequence.

The lexer identifies language tokens such as keywords, identifiers, integer literals, operators, and punctuation.

It also rejects unsupported preprocessing directives and backslash-newline line splicing. Directive-like text inside comments is treated as comment content.

## 4. Syntax Analysis and AST

**Source file:** `src/parser.py`

The parser is a student-developed recursive descent parser. It consumes lexer tokens and constructs an Abstract Syntax Tree.

Important AST node classes include:

- `Program`
- `Function`
- `FunctionPrototype`
- `Parameter`
- `VariableDeclaration`
- `Block`
- `ReturnStatement`
- `IfStatement`
- `WhileStatement`
- `ForStatement`
- `BreakStatement`
- `ContinueStatement`
- `BinaryOperation`
- `UnaryOperation`
- `Assignment`
- `FunctionCall`
- `Number`
- `Identifier`

Important parser methods include:

- `parse_program()` — parses the complete program.
- `parse_function()` — parses function declarations and definitions.
- `parse_block()` — parses compound statements.
- `parse_statement()` — parses supported statements.
- `parse_expression()` — starts expression parsing.
- `parse_assignment()` — handles assignment expressions.
- `parse_logical_or()` and `parse_logical_and()` — handle logical operators.
- `parse_equality()` and `parse_relational()` — handle comparisons.
- `parse_additive()` and `parse_multiplicative()` — handle arithmetic precedence.
- `parse_unary()` and `parse_primary()` — handle unary and primary expressions.

Separate parsing methods implement operator precedence rather than treating every operator at the same level.

## 5. Semantic Analysis and Symbol Management

**Source file:** `src/semantic.py`

Semantic analysis checks whether the parsed program follows the supported language rules.

Main components:

- `SemanticError` — represents semantic errors.
- `Symbol` — stores information about declared symbols.
- `FunctionInfo` — stores function information.
- `Scope` — represents a scope and its symbol lookup.
- `SymbolTable` — manages scopes and declarations.
- `SemanticAnalyzer` — performs semantic analysis.

Important methods include:

- `collect_functions()` — collects function declarations and definitions.
- `analyze_function()` — analyzes a function.
- `analyze_block()` — analyzes statements inside a block.
- `analyze_statement()` — checks statement semantics.
- `analyze_expression()` — checks expression semantics.
- `require_int()` — checks integer requirements.

The symbol table supports scope creation, scope entry and exit, symbol declaration, and lookup. This allows the compiler to handle local variables and nested scopes.

Semantic checks cover supported declarations, function usage, expressions, assignments, and control-flow constructs.

## 6. Student-Developed Intermediate Representation

**Source file:** `src/ir.py`

After semantic analysis, the compiler generates its own intermediate representation.

Main components:

- `IRInstruction` — represents an IR instruction.
- `IRFunction` — represents a function's instructions.
- `IRProgram` — represents the complete intermediate program.
- `IRGenerator` — generates the intermediate representation.

Important methods include:

- `generate()` — generates IR for a program.
- `generate_function()` — generates IR for a function.
- `generate_block()` — generates IR for a block.
- `generate_statement()` — generates IR for statements.
- `generate_expression()` — generates IR for expressions.
- `generate_logical_and()` — generates short-circuit logical AND.
- `generate_logical_or()` — generates short-circuit logical OR.
- `new_temp()` — creates temporary values.
- `new_label()` — creates control-flow labels.
- `emit()` — appends an IR instruction.
- `print_ir()` — displays the student IR.

The IR provides an intermediate stage between the AST and LLVM backend. It represents operations, temporary values, labels, branches, and function-related instructions.

Logical AND and OR use control-flow-based generation to support short-circuit evaluation.

## 7. LLVM Backend

**Source file:** `src/llvm_backend.py`

The LLVM backend converts the student-developed IR into LLVM Intermediate Representation.

Main component:

- `LLVMBackend`

Important methods include:

- `generate()` — generates LLVM IR for the program.
- `generate_function()` — generates LLVM IR for a function.
- `generate_binary()` — handles binary operations.
- `generate_unary()` — handles unary operations.
- `generate_call()` — handles function calls.
- `add_value()` and `get_value()` — manage generated values.

The backend produces LLVM IR, which is passed to LLVM `llc` to generate x86-64 assembly.

LLVM is used for backend code generation. The lexer, parser, semantic analyzer, and student IR are implemented within this project.

## 8. Command-Line Interface

**Source file:** `src/main.py`

The CLI provides the main interface for compiling programs and inspecting compiler stages.

Important functions:

- `compile_lexer()` — invokes lexical analysis.
- `compile_parser()` — invokes parsing.
- `compile_semantics()` — invokes semantic analysis.
- `generate_student_ir()` — generates student IR.
- `generate_llvm_ir()` — invokes LLVM IR generation.
- `format_student_ir()` — formats student IR for display.
- `show_capabilities()` — displays compiler capabilities.
- `create_argument_parser()` — configures command-line arguments.
- `main()` — controls the compilation workflow.

Supported operations include compiler version and help information, capability reporting, source checking, stage dumps, backend IR output, backend selection, and assembly output-path selection.

The implemented backend is LLVM. QBE is not implemented.

## 9. Error Handling

The compiler reports errors encountered during compilation.

The implementation includes:

- Lexical rejection of unsupported preprocessing directives and line splicing.
- Parser errors for invalid syntax.
- Semantic errors for invalid declarations and operations.
- CLI error handling for compilation and backend failures.
- Handling for missing files or required external tools.

Semantic errors are assigned categories by the `SemanticError` classifier. The current classification is message-based, so it should not be described as a complete structured diagnostic system with every SRS-required field unless separately verified.

## 10. Testing Strategy

The project includes automated tests in the `tests/` directory.

| Test file | Main purpose |
|---|---|
| `test_lexer.py` | Tokenization and lexical behavior |
| `test_parser.py` | Parsing and AST construction |
| `test_semantic.py` | Semantic checks and scopes |
| `test_ir.py` | Student IR generation |
| `test_llvm_backend.py` | LLVM backend generation |
| `test_fuzz.py` | Malformed-input robustness |
| `test_end_to_end.py` | Compilation, native execution and runtime behavior |

The latest recorded full test run completed with:

```text
Ran 109 tests in 8.486s

OK
```

The end-to-end tests compile seven example programs, link their generated assembly with GCC, execute them, and compare their exit statuses with expected results.

A separate runtime test checks short-circuit behavior for logical AND and OR.

## 11. Development Environment

The development environment uses:

- Python 3
- Ubuntu Linux
- LLVM 21.1.8
- LLVM `llc`
- GCC
- x86-64 target architecture

The installed tool versions should be checked again in the final submission environment.

## 12. Current Limitations

- Only the specified C Minor subset is supported.
- The compiler does not implement the complete C language.
- Preprocessing is disabled.
- QBE backend support is not implemented.
- The target is x86-64 Linux.
- Semantic diagnostic classification is currently message-based.
- Full SRS diagnostic and evidence requirements still require a separate final audit.

## 13. Conclusion

The project demonstrates a complete basic compiler pipeline using student-developed lexical analysis, recursive descent parsing, AST construction, semantic analysis, symbol management, and intermediate representation generation.

LLVM is integrated as the backend technology for generating native assembly. Automated unit, robustness, and end-to-end tests provide verification of the implemented compiler components.

This report describes the current implementation and does not claim that requirements without supporting evidence have been fully satisfied.
