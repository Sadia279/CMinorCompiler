# Compiler Evidence Index

This folder contains generated outputs and test evidence from the C Minor Compiler.

## Successful Compilation Evidence

| File | Evidence |
|---|---|
| `capabilities.txt` | Compiler capabilities and detected toolchain |
| `tokens.txt` | Lexer token output |
| `ast.txt` | Parser AST output |
| `symbols.txt` | Symbol information |
| `student_ir.txt` | Project intermediate representation |
| `llvm_ir.txt` | LLVM IR output |
| `cli_test.ll` | LLVM IR for the CLI example |
| `cli_test.s` | Generated x86-64 assembly |
| `cli_test.o` | Assembled object file |
| `cli_test` | Linked executable |
| `execution.txt` | Example program execution result |
| `srs_b3.s` | Assembly for the recursive-function example |
| `srs_b3.ll` | LLVM IR for the recursive-function example |
| `srs_b3_execution.txt` | Recursive example execution result |
| `tool_versions.txt` | Recorded Python, GCC and LLVM versions |
| `toolchain_versions.txt` | Toolchain and target details |

## Negative Compilation Evidence

| File | Evidence |
|---|---|
| `undeclared_variable.cm` | Source containing an undeclared variable |
| `undeclared_stderr.txt` | Diagnostic for the undeclared variable |
| `undeclared_exit_status.txt` | Compiler exit status |
| `preprocessor_rejected.cm` | Source containing an unsupported directive |
| `preprocessor_stderr.txt` | Rejection diagnostic |
| `preprocessor_exit_status.txt` | Compiler exit status |

## Test and Robustness Evidence

| File | Evidence |
|---|---|
| `full_test_results.txt` | Earlier full automated test run: 109 test methods |
| `final_test_results.txt` | Latest final full automated test run: 109 test methods |
| `fuzz_test_results.txt` | Malformed-input test: 100 distinct inputs |
| `test_inventory.txt` | Inventory of test methods and example programs |
| `acceptance_cases.md` | 50 mapped positive and negative behavior checks |
| `reproducibility.txt` | Repeated stage-output comparison |

## Academic Integrity and Disclosure

| File | Evidence |
|---|---|
| `../AI_AND_ACADEMIC_INTEGRITY_DISCLOSURE.md` | Disclosure of AI assistance used during development |

## Reproduction

From the project root:

        venv/bin/python -m src.main --capabilities
    venv/bin/python -m unittest discover -s tests -v
    venv/bin/python -m unittest tests.test_fuzz -v

To reproduce the successful CLI example:

    venv/bin/python -m src.main examples/cli_test.cm -o docs/evidence/cli_test.s
    gcc -c docs/evidence/cli_test.s -o docs/evidence/cli_test.o
    gcc -no-pie docs/evidence/cli_test.o -o docs/evidence/cli_test
    docs/evidence/cli_test

The expected exit status of `cli_test` is 30.

These files are development evidence. Use the teacher-provided SRS as the reference for the requirement-by-requirement review. The SRS PDF is a reference document, not a project file to copy into this folder.


## Related submission disclosures

- `../AI_AND_ACADEMIC_INTEGRITY_DISCLOSURE.md`: AI assistance disclosure.
- `../THIRD_PARTY_NOTICES.md`: Python dependencies and external toolchain notice.
