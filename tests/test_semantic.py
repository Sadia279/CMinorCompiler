
import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer, SemanticError


class TestSemanticAnalyzer(unittest.TestCase):

    def analyze_code(self, code):
        tokens = Lexer(code).tokenize()
        tree = Parser(tokens).parse()
        return SemanticAnalyzer().analyze(tree)

    def test_valid_main_function(self):
        self.assertTrue(
            self.analyze_code("int main(void) { return 0; }")
        )

    def test_valid_function_call(self):
        code = (
            "int add(int a, int b) { return a + b; } "
            "int main(void) { return add(10, 20); }"
        )
        self.assertTrue(self.analyze_code(code))

    def test_parameter_assignment(self):
        code = (
            "int change(int x) { x = 20; return x; } "
            "int main(void) { return change(10); }"
        )
        self.assertTrue(self.analyze_code(code))

    def test_variable_shadowing(self):
        code = (
            "int main(void) { int x = 10; "
            "{ int x = 20; } return x; }"
        )
        self.assertTrue(self.analyze_code(code))

    def test_duplicate_variable(self):
        code = (
            "int main(void) { int x = 10; "
            "int x = 20; return x; }"
        )
        with self.assertRaisesRegex(SemanticError, "Duplicate declaration"):
            self.analyze_code(code)

    def test_undeclared_variable(self):
        code = "int main(void) { return x; }"

        with self.assertRaisesRegex(
            SemanticError,
            r"Undeclared variable 'x' at line 1, column 25"
        ):
            self.analyze_code(code)

    def test_undefined_function(self):
        code = "int main(void) { return calculate(10); }"
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'calculate' called before declaration "
            r"or not declared at line 1, column 25"
        ):
            self.analyze_code(code)

    def test_wrong_argument_count(self):
        code = (
            "int add(int a, int b) { return a + b; } "
            "int main(void) { return add(10); }"
        )
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_break_outside_loop(self):
        code = "int main(void) { break; return 0; }"
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_continue_outside_loop(self):
        code = "int main(void) { continue; return 0; }"
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_invalid_main_return_type(self):
        code = "void main(void) { return; }"
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_seven_parameters_rejected(self):
        code = (
            "int add(int a, int b, int c, int d, "
            "int e, int f, int g) { return a; } "
            "int main(void) { return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'add' cannot have more than 6 parameters "
            r"at line 1, column 5"
        ):
            self.analyze_code(code)

    def test_void_function_cannot_return_value(self):
        code = (
            "void display(void) { return 10; } "
            "int main(void) { return 0; }"
        )
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_int_function_must_return_value(self):
        code = "int main(void) { return; }"
        with self.assertRaises(SemanticError):
            self.analyze_code(code)

    def test_matching_prototype_and_definition(self):
        code = (
            "int add(int a, int b); "
            "int add(int a, int b) { return a + b; } "
            "int main(void) { return add(10, 20); }"
        )
        self.assertTrue(self.analyze_code(code))

    def test_mismatched_prototype_and_definition(self):
        code = (
            "int add(int a, int b); "
            "int add(int a) { return a; } "
            "int main(void) { return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Conflicting declaration of function 'add' "
            r"at line 1, column 28"
        ):
            self.analyze_code(code)

    def test_duplicate_function_definition(self):
        code = (
            "int add(void) { return 10; } "
            "int add(void) { return 20; } "
            "int main(void) { return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'add' is defined more than once "
            r"at line 1, column 34"
        ):
            self.analyze_code(code)

    def test_prototype_without_definition(self):
        code = (
            "int add(int a, int b); "
            "int main(void) { return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'add' was declared but not defined "
            r"at line 1, column 5"
        ):
            self.analyze_code(code)


    def analyze_with_symbols(self, code):
        tokens = Lexer(code).tokenize()
        tree = Parser(tokens).parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(tree)
        return analyzer

    def test_function_scope_is_recorded(self):
        code = "int main(void) { int x = 10; return x; }"
        analyzer = self.analyze_with_symbols(code)

        scopes = analyzer.symbol_table.scopes

        self.assertEqual(len(scopes), 2)
        self.assertIn("x", scopes[1].symbols)
        self.assertEqual(scopes[1].symbols["x"].scope_id, 1)

    def test_nested_block_scope_is_recorded(self):
        code = (
            "int main(void) { int x = 10; "
            "{ int y = 20; } return x; }"
        )
        analyzer = self.analyze_with_symbols(code)

        scopes = analyzer.symbol_table.scopes

        self.assertEqual(len(scopes), 3)
        self.assertIs(scopes[2].parent, scopes[1])
        self.assertIn("y", scopes[2].symbols)

    def test_for_loop_scope_is_recorded(self):
        code = (
            "int main(void) { "
            "for (int i = 0; i < 3; i = i + 1) { "
            "int z = i; } return 0; }"
        )
        analyzer = self.analyze_with_symbols(code)

        scopes = analyzer.symbol_table.scopes

        self.assertEqual(len(scopes), 4)
        self.assertIs(scopes[2].parent, scopes[1])
        self.assertIs(scopes[3].parent, scopes[2])
        self.assertIn("i", scopes[2].symbols)
        self.assertIn("z", scopes[3].symbols)

    def test_shadowed_variables_belong_to_different_scopes(self):
        code = (
            "int main(void) { int x = 10; "
            "{ int x = 20; } return x; }"
        )
        analyzer = self.analyze_with_symbols(code)

        scopes = analyzer.symbol_table.scopes
        outer_x = scopes[1].symbols["x"]
        inner_x = scopes[2].symbols["x"]

        self.assertNotEqual(outer_x.scope_id, inner_x.scope_id)
        self.assertEqual(outer_x.scope_id, 1)
        self.assertEqual(inner_x.scope_id, 2)


    def test_scope_types_and_function_ownership(self):
        code = (
            "int main(void) { "
            "int x = 10; "
            "{ int y = 20; } "
            "for (int i = 0; i < 2; i = i + 1) "
            "{ int z = i; } "
            "return x; }"
        )
        analyzer = self.analyze_with_symbols(code)
        scopes = analyzer.symbol_table.scopes

        self.assertEqual(scopes[0].scope_type, "global")
        self.assertEqual(scopes[1].scope_type, "function")
        self.assertEqual(scopes[2].scope_type, "block")
        self.assertEqual(scopes[3].scope_type, "for")
        self.assertEqual(scopes[4].scope_type, "block")

        for scope in scopes[1:]:
            self.assertEqual(scope.function_name, "main")

    def test_multiple_functions_have_correct_scope_owners(self):
        code = (
            "int first(void) { int a = 1; return a; } "
            "int main(void) { int b = 2; return b; }"
        )
        analyzer = self.analyze_with_symbols(code)
        scopes = analyzer.symbol_table.scopes

        self.assertEqual(scopes[1].scope_type, "function")
        self.assertEqual(scopes[1].function_name, "first")
        self.assertEqual(scopes[2].scope_type, "function")
        self.assertEqual(scopes[2].function_name, "main")


    def test_variable_outside_block_scope_is_rejected(self):
        code = (
            "int main(void) { "
            "{ int x = 10; } "
            "return x; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Undeclared variable 'x'"
        ):
            self.analyze_code(code)

    def test_for_initializer_variable_outside_loop_is_rejected(self):
        code = (
            "int main(void) { "
            "for (int i = 0; i < 3; i = i + 1) { } "
            "return i; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Undeclared variable 'i'"
        ):
            self.analyze_code(code)

    def test_function_call_before_declaration_is_rejected(self):
        code = (
            "int main(void) { return add(10, 20); } "
            "int add(int a, int b) { return a + b; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'add' called before declaration"
        ):
            self.analyze_code(code)

    def test_too_many_function_arguments(self):
        code = (
            "int add(int a, int b) { return a + b; } "
            "int main(void) { return add(1, 2, 3); }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Function 'add' expects 2 arguments, but got 3"
        ):
            self.analyze_code(code)

    def test_assignment_to_number_is_rejected(self):
        code = "int main(void) { 10 = 20; return 0; }"
        with self.assertRaisesRegex(
            SemanticError,
            r"Assignment target must be a variable"
        ):
            self.analyze_code(code)

    def test_duplicate_parameter_names_are_rejected(self):
        code = (
            "int add(int value, int value) { return value; } "
            "int main(void) { return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Duplicate declaration of 'value'"
        ):
            self.analyze_code(code)

    def test_variable_used_before_declaration_is_rejected(self):
        code = (
            "int main(void) { "
            "int result = value; "
            "int value = 10; "
            "return result; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Undeclared variable 'value'"
        ):
            self.analyze_code(code)


    def test_void_call_cannot_initialize_int_variable(self):
        code = (
            "void display(void) { return; } "
            "int main(void) { int x = display(); return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"Variable initializer requires an int expression"
        ):
            self.analyze_code(code)

    def test_void_call_cannot_be_if_condition(self):
        code = (
            "void display(void) { return; } "
            "int main(void) { if (display()) return 1; return 0; }"
        )
        with self.assertRaisesRegex(
            SemanticError,
            r"If condition requires an int expression"
        ):
            self.analyze_code(code)

    def test_function_call_after_prototype(self):
        code = (
            "int add(int a, int b); "
            "int main(void) { return add(10, 20); } "
            "int add(int a, int b) { return a + b; }"
        )
        self.assertTrue(self.analyze_code(code))

    def test_break_and_continue_in_nested_loops(self):
        code = (
            "int main(void) { "
            "int i = 0; "
            "while (i < 3) { "
            "int j = 0; "
            "while (j < 3) { "
            "j = j + 1; "
            "if (j == 1) continue; "
            "if (j == 2) break; "
            "} "
            "i = i + 1; "
            "} "
            "return 0; }"
        )
        self.assertTrue(self.analyze_code(code))


if __name__ == "__main__":
    unittest.main()
