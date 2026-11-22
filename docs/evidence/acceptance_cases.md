# C Minor Compiler — Acceptance Case Inventory

This inventory maps 50 distinct positive and negative checks to existing automated tests. It is based on the current test suite; it does not claim that every case is a separate end-to-end program.

**Recorded suite result:** 109 test methods passed (`Ran 109 tests in 8.486s`, as recorded in `SRS_TRACEABILITY.md`).

**Separate robustness requirement:** `tests/test_fuzz.py` checks 100 distinct malformed inputs, each with a 5-second timeout. These are not added to the 50 cases below.

| ID | Area | Type | Scenario / expected behavior | Existing test |
|---|---|---|---|---|
| AC-001 | Lexer | Positive | Recognize keywords and identifiers | `test_keywords_and_identifiers` |
| AC-002 | Lexer | Positive | Recognize decimal numbers and operators | `test_numbers_and_operators` |
| AC-003 | Lexer | Positive | Recognize logical operators | `test_logical_operators` |
| AC-004 | Lexer | Positive | Recognize comparison operators | `test_comparison_operators` |
| AC-005 | Lexer | Positive | Ignore line comments | `test_comments_are_ignored` |
| AC-006 | Lexer | Positive | Ignore block comments | `test_block_comments_are_ignored` |
| AC-007 | Lexer | Positive | Keep identifiers separated by a block comment distinct | `test_block_comment_between_identifiers` |
| AC-008 | Lexer | Negative | Reject unterminated block comments | `test_unterminated_block_comment` |
| AC-009 | Lexer | Negative | Reject invalid source characters | `test_invalid_character` |
| AC-010 | Lexer | Negative | Reject preprocessing directives | `test_preprocessor_directive_is_rejected` |
| AC-011 | Parser | Positive | Parse a function definition | `test_function_definition` |
| AC-012 | Parser | Positive | Parse a variable declaration | `test_variable_declaration` |
| AC-013 | Parser | Positive | Parse if/else statements | `test_if_else_statement` |
| AC-014 | Parser | Positive | Parse while loops | `test_while_loop` |
| AC-015 | Parser | Positive | Parse for loops | `test_for_loop` |
| AC-016 | Parser | Positive | Parse function calls | `test_function_call` |
| AC-017 | Parser | Negative | Reject invalid syntax | `test_invalid_syntax` |
| AC-018 | Parser | Positive | Parse function prototypes | `test_function_prototype` |
| AC-019 | Parser | Positive | Parse break and continue statements | `test_break_and_continue` |
| AC-020 | Parser | Positive | Apply arithmetic operator precedence | `test_operator_precedence` |
| AC-021 | Semantic | Positive | Accept a valid main function | `test_valid_main_function` |
| AC-022 | Semantic | Positive | Accept a valid function call | `test_valid_function_call` |
| AC-023 | Semantic | Positive | Permit assignment to a function parameter | `test_parameter_assignment` |
| AC-024 | Semantic | Positive | Permit variable shadowing in nested scope | `test_variable_shadowing` |
| AC-025 | Semantic | Negative | Reject duplicate variable declarations | `test_duplicate_variable` |
| AC-026 | Semantic | Negative | Reject use of an undeclared variable | `test_undeclared_variable` |
| AC-027 | Semantic | Negative | Reject calls to undefined functions | `test_undefined_function` |
| AC-028 | Semantic | Negative | Reject a function call with the wrong argument count | `test_wrong_argument_count` |
| AC-029 | Semantic | Negative | Reject break outside a loop | `test_break_outside_loop` |
| AC-030 | Semantic | Negative | Reject continue outside a loop | `test_continue_outside_loop` |
| AC-031 | Semantic | Negative | Reject an invalid main return type | `test_invalid_main_return_type` |
| AC-032 | Semantic | Negative | Reject a function with seven parameters | `test_seven_parameters_rejected` |
| AC-033 | Semantic | Negative | Reject a value returned from a void function | `test_void_function_cannot_return_value` |
| AC-034 | Semantic | Negative | Reject a missing value in an int function return | `test_int_function_must_return_value` |
| AC-035 | Semantic | Positive | Accept a matching function prototype and definition | `test_matching_prototype_and_definition` |
| AC-036 | Semantic | Negative | Reject mismatched prototype and definition | `test_mismatched_prototype_and_definition` |
| AC-037 | Semantic | Negative | Reject duplicate function definitions | `test_duplicate_function_definition` |
| AC-038 | Semantic | Negative | Reject use of a variable outside its block scope | `test_variable_outside_block_scope_is_rejected` |
| AC-039 | IR | Positive | Allocate distinct storage for shadowed variables | `test_shadowed_variables_use_distinct_storage` |
| AC-040 | IR | Positive | Assign to the nearest shadowed variable | `test_assignment_updates_nearest_shadowed_variable` |
| AC-041 | IR | Positive | Give function parameters internal storage identities | `test_function_parameter_uses_internal_name` |
| AC-042 | IR | Positive | Keep for-loop variables in separate scope | `test_for_loop_variable_has_separate_scope` |
| AC-043 | IR | Positive | Lower logical AND using a short-circuit jump | `test_logical_and_uses_short_circuit_jump` |
| AC-044 | IR | Positive | Lower logical OR using a short-circuit jump | `test_logical_or_uses_short_circuit_jump` |
| AC-045 | LLVM backend | Positive | Generate LLVM IR for integer addition | `test_generates_addition` |
| AC-046 | LLVM backend | Positive | Generate LLVM IR for subtraction | `test_generates_subtraction` |
| AC-047 | LLVM backend | Positive | Generate LLVM IR for multiplication | `test_generates_multiplication` |
| AC-048 | LLVM backend | Positive | Generate signed integer division | `test_generates_signed_division` |
| AC-049 | LLVM backend | Positive | Generate signed remainder operation | `test_generates_signed_remainder` |
| AC-050 | LLVM backend | Positive | Generate a function call in LLVM IR | `test_generates_function_call` |

## Interpretation and limitations

- The 50 entries are distinct behavior checks mapped to existing test methods.
- A method passing as part of the full test suite is the recorded evidence; this table does not claim a separate test run for each row.
- The 100 malformed-input checks are reported separately and are not counted toward this 50-case inventory.
- End-to-end execution evidence is separately available in the project evidence folder.
- This inventory alone does not prove every compulsory SRS requirement is satisfied. Requirement-by-requirement traceability remains necessary.
