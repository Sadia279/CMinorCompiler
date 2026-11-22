# C Minor Compiler — Complete SRS Traceability Ledger

**Reference:** C Minor Compiler SRS Version 1.0, 9 October 2026  
**Total compulsory requirements:** 98  
**Rule:** A requirement is not verified merely because a related feature exists.

## Status definitions

- **Verified:** Acceptance condition demonstrated by implementation and evidence.
- **Partial:** Some evidence exists, but the full acceptance condition is not demonstrated.
- **Pending audit:** Must be inspected and tested against the original SRS.

## 1. Complete compulsory requirement register

| Requirement ID | Required acceptance check | Implementation / evidence to inspect | Status |
|---|---|---|---|
| CM-SCP-001 | All compulsory programs accepted; invalid programs rejected | All compiler stages and acceptance tests | Pending audit |
| CM-SCP-002 | Student-owned lexer, parser, semantics, IR and lowering | `src/lexer.py`, `parser.py`, `semantic.py`, `ir.py`, `llvm_backend.py` | Pending audit |
| CM-SCP-003 | One self-contained `.cm` or `.c`; preprocessing rejected | Lexer and directive tests | Partial |
| CM-SCP-004 | Generate `.s`, independently assemble, link and execute | `docs/evidence/` | Partial |
| CM-SCP-005 | Follow C Minor teaching profile, not claim full C23 | README and language implementation | Pending audit |
| CM-SCP-006 | Complete source-to-executable trace with loop and function call | Evidence folder and examples | Partial |
| CM-SCP-007 | Approved public dependencies and reproducible procedures | `requirements.txt`, README | Pending audit |
| EXT-001 | Implementation uses an approved language | Python source | Partial |
| EXT-002 | Student-authored scanner, grammar, AST and error handling | Lexer and parser source | Partial |
| EXT-003 | Student-owned semantic checks, IR and lowering | Semantic and backend source | Pending audit |
| EXT-004 | Use exactly one approved backend family | LLVM backend and capabilities | Partial |
| EXT-005 | Backend does not replace student language semantics | `src/llvm_backend.py`, `src/ir.py` | Pending audit |
| EXT-006 | GCC/Clang only receive generated assembly/object files | End-to-end tests and commands | Partial |
| EXT-007 | No preprocessing in source pipeline | Lexer and directive tests | Partial |
| EXT-008 | Reproducible build and test procedure with results | README, evidence, test output | Partial |
| EXT-009 | Disclose third-party code and AI assistance | AI disclosure created; third-party code audit pending | Partial |
| EXT-010 | No project-specific runtime; same-file function calls | Semantic and execution tests | Pending audit |
| CM-LANG-001 | Signed 32-bit int and permitted void usage | Semantic and backend tests | Pending audit |
| CM-LANG-002 | Valid compilation unit and exactly one `int main(void)` | Parser and semantic tests | Pending audit |
| CM-LANG-003 | 0–6 parameters, declaration-before-call, recursion | Semantic and end-to-end tests | Pending audit |
| CM-LANG-004 | Scalar locals, initialization, shadowing and for scope | Semantic and IR tests | Pending audit |
| CM-LANG-005 | Execution result determined by process exit status | End-to-end tests | Partial |
| CM-LANG-006 | Capabilities documents exclusions and limits | `capabilities.txt` | Partial |
| CM-LEX-001 | ASCII identifiers, keywords and source locations | `src/lexer.py`, lexer tests | Pending audit |
| CM-LEX-002 | Decimal literal rules and range checking | Lexer tests | Pending audit |
| CM-LEX-003 | Whitespace, comments, token boundaries and unterminated comments | Lexer tests | Pending audit |
| CM-LEX-004 | Required operators and longest-token matching | Lexer tests | Pending audit |
| CM-LEX-005 | `#` and `%:` directive-position handling | Lexer tests | Partial |
| CM-LEX-006 | LF/CRLF locations, line-splicing rejection and non-ASCII errors | Lexer tests | Pending audit |
| CM-LEX-007 | Controlled errors for invalid characters and literals | Lexer and fuzz tests | Pending audit |
| CM-SYN-001 | Every compulsory grammar production and precedence rule | `src/parser.py`, parser tests | Pending audit |
| CM-SYN-002 | Inspectable AST for all required constructs | AST dump and parser tests | Partial |
| CM-SYN-003 | Source spans and deterministic AST output | Parser and AST dump | Pending audit |
| CM-SYN-004 | Declaration placement and dangling-else behavior | Parser tests | Pending audit |
| CM-SYN-005 | Controlled syntax recovery without successful invalid output | Parser and fuzz tests | Pending audit |
| CM-SEM-001 | Function lookup, parameter, block and for scopes | `src/semantic.py`, semantic tests | Pending audit |
| CM-SEM-002 | Declaration order, uniqueness, shadowing and prototypes | Semantic tests | Pending audit |
| CM-SEM-003 | Expression types, lvalues and void-value rejection | Semantic tests | Pending audit |
| CM-SEM-004 | Calls, break/continue, returns and main signature | Semantic tests | Pending audit |
| CM-SEM-005 | Semantic errors prevent final assembly generation | CLI and semantic tests | Pending audit |
| CM-SEM-006 | Symbol dump includes required identity and location details | `symbols.txt`, CLI tests | Partial |
| CM-SEM-007 | Runtime tests avoid undefined behavior | End-to-end test review | Pending audit |
| CM-EXP-001 | All compulsory expression forms supported | Parser, semantic and IR tests | Pending audit |
| CM-EXP-002 | Precedence, associativity and assignment lvalue rules | Parser and semantic tests | Pending audit |
| CM-EXP-003 | Integer expression results and boolean normalization | IR and backend tests | Pending audit |
| CM-EXP-004 | Signed division/remainder behavior and safe test operands | Runtime tests | Pending audit |
| CM-EXP-005 | Logical AND/OR short-circuit evaluation | End-to-end short-circuit test | Partial |
| CM-EXP-006 | Left-to-right operand/call sequencing | IR and runtime tests | Pending audit |
| CM-EXP-007 | Nested calls and assignment sequencing preserved | IR and backend tests | Pending audit |
| CM-EXP-008 | Signed 32-bit behavior in lowered IR | LLVM backend tests | Pending audit |
| CM-STM-001 | Blocks, declarations, statements and control flow | Parser and IR tests | Pending audit |
| CM-STM-002 | For initializer, optional condition/update and scope | Parser, semantic and IR tests | Pending audit |
| CM-STM-003 | Correct break and continue destinations | IR and runtime tests | Pending audit |
| CM-STM-004 | Int/void functions, prototypes, recursion and main | Semantic and end-to-end tests | Pending audit |
| CM-STM-005 | Correct return forms and return-type checking | Semantic tests | Pending audit |
| CM-STM-006 | Explicit final top-level return in int functions | Semantic tests | Pending audit |
| CM-IR-001 | Separate documented student-developed IR | `src/ir.py`, `student_ir.txt` | Partial |
| CM-IR-002 | IR represents values, identities, operations, calls and returns | IR implementation and tests | Pending audit |
| CM-IR-003 | IR preserves control flow, recursion and short circuit | IR and end-to-end tests | Pending audit |
| CM-IR-004 | Deterministic, independently inspectable IR dump | `student_ir.txt`, IR tests | Partial |
| CM-CG-001 | Student IR translated to valid LLVM IR or QBE IL | `src/llvm_backend.py`, `llvm_ir.txt` | Partial |
| CM-CG-002 | Correct variable, branch, call and return lowering | Backend tests | Pending audit |
| CM-CG-003 | Correct signed integer and boolean representation | Backend tests | Pending audit |
| CM-CG-004 | Backend emits assembly; assembler and linker produce executable | `cli_test.s`, `.o`, executable | Partial |
| CM-CG-005 | Capabilities and backend selection report only supported backends | `main.py`, capabilities output | Partial |
| CM-CG-006 | Required LLVM baseline command and target flags | `src/main.py` | Partial |
| CM-CG-007 | Backend failure handling, atomic output replacement and cleanup | CLI/backend failure tests | Pending audit |
| CM-CG-008 | Standard Linux startup and main ABI | Linked executable and runtime tests | Pending audit |
| CM-CG-009 | Student-owned IR-to-backend lowering | `src/llvm_backend.py` | Pending audit |
| CM-CLI-001 | Runnable `cminorcc` command and default `.s` output | `cminorcc`, CLI tests | Partial |
| CM-CLI-002 | All required CLI actions and backend selection | `src/main.py` | Partial |
| CM-CLI-003 | Deterministic dumps, output paths and incompatible-option errors | CLI tests | Pending audit |
| CM-CLI-004 | Language version, target, backend versions, limits and exclusions | `capabilities.txt` | Partial |
| CM-CLI-005 | Exit codes 0/1/2 and correct stdout/stderr separation | CLI tests | Pending audit |
| CM-DIA-001 | Category, severity, file, line and column in source errors | Lexer, parser, semantic and CLI diagnostics | Partial |
| CM-DIA-002 | All required diagnostic categories distinguished | Diagnostic tests and error handling | Partial |
| CM-DIA-003 | Directive rejection and valid directive-like comments | Lexer tests | Partial |
| CM-DIA-004 | Controlled parser, I/O, resource and backend failures | Fuzz and CLI tests | Partial |
| CM-NFR-001 | Offline Linux x86-64 build/test after dependency installation | README and environment evidence | Pending audit |
| CM-NFR-002 | All required minimum input capacities work | Manual boundary checks and capabilities | Partial |
| CM-NFR-003 | 100 distinct malformed inputs, each with 5-second timeout | `tests/test_fuzz.py` | Partial |
| CM-NFR-004 | Reproducible stage dumps, IR and backend IL | Repeat-run comparison required | Pending audit |
| CM-NFR-005 | Safe structured external process invocation | `subprocess.run` argument list in `src/main.py` | Partial |
| CM-VER-001 | Every compulsory ID has checks, expected/observed results and evidence | This ledger | Pending audit |
| CM-VER-002 | At least 50 distinct positive/negative cases covering all listed areas | `docs/evidence/acceptance_cases.md` (50 mapped checks; full coverage audit pending) | Partial |
| CM-VER-003 | Full student pipeline through assembler/linker; no C source compiled by GCC | End-to-end tests and build commands | Partial |
| CM-VER-004 | Reproducible commands, tool versions and exit statuses | README and `tool_versions.txt` | Partial |
| CM-VER-005 | No undefined behavior in positive runtime tests; useful negative diagnostics | Test and diagnostic review | Pending audit |
| CM-VER-006 | Clean build, full acceptance, evidence and student walkthrough | Final acceptance checklist | Pending audit |
| CM-DEL-001 | Source, runnable command, dependencies, versions and instructions | Project root, `requirements.txt`, README | Partial |
| CM-DEL-002 | Complete user guide including grammar, flags, exits, target and limits | README | Pending audit |
| CM-DEL-003 | Developer report with design and code pointers | `docs/DEVELOPER_REPORT.md` | Partial |
| CM-DEL-004 | All stage outputs plus loop/function execution trace and failures | `docs/evidence/` | Partial |
| CM-DEL-005 | Tests, ledger, packages, licenses and academic-integrity disclosure | Tests, ledger and disclosure | Pending audit |
| CM-DEL-006 | Self-contained source, tests, docs and reproduction instructions | Project root | Partial |
| CM-CHG-001 | Compulsory changes follow documented course-wide amendments | SRS change-control review | Pending audit |
| CM-CHG-002 | Optional features preserve baseline and are disclosed | Capabilities and documentation | Pending audit |
| CM-CHG-003 | Every corrected compulsory defect has a regression test | Test history and regression suite | Pending audit |

## 2. Existing evidence inventory

| Evidence | Location | Current observation |
|---|---|---|
| Capabilities | `docs/evidence/capabilities.txt` | Captured |
| Tokens | `docs/evidence/tokens.txt` | Captured |
| AST | `docs/evidence/ast.txt` | Captured |
| Symbols | `docs/evidence/symbols.txt` | Captured |
| Student IR | `docs/evidence/student_ir.txt` | Captured |
| LLVM IR | `docs/evidence/llvm_ir.txt`, `cli_test.ll` | Captured |
| Assembly | `docs/evidence/cli_test.s` | Captured |
| Object | `docs/evidence/cli_test.o` | Captured |
| Executable | `docs/evidence/cli_test` | Captured |
| Execution status | `docs/evidence/execution.txt` | Captured |
| Tool versions | `docs/evidence/tool_versions.txt` | Captured |
| Undeclared variable diagnostic | `docs/evidence/undeclared_stderr.txt` | Captured; exit 1 |
| Directive rejection | `docs/evidence/preprocessor_stderr.txt` | Captured; exit 1 |

## 3. Previously observed test result

The explicitly named test modules were run successfully:

```text
Ran 109 tests in 8.486s

OK
```

This confirms the test suite passed at that point. It does not by itself prove 50 distinct acceptance cases.

## 4. Known remaining checks

1. Audit all 98 rows against actual source and test cases.
2. Count distinct positive and negative cases, not merely unittest methods.
3. Confirm the 100 malformed-input corpus and per-case timeout.
4. Verify all diagnostic fields and required categories.
5. Verify output preservation and atomic `.s` replacement on backend failure.
6. Add a source-to-executable trace that explicitly covers a loop and a function call.
7. Compare deterministic outputs across repeated runs.
8. Confirm dependency versions/download sources and academic-integrity disclosure.
9. Run final acceptance tests and retain fresh output.

## 5. Evidence integrity

This register is complete by requirement ID, but it is **not a declaration of full compliance**. Partial and pending statuses must only be changed after the corresponding implementation, expected behavior, observed result and evidence have been checked against SRS Version 1.0.
