import unittest

from src.lexer import Lexer
from src.parser import (
    Parser,
    Function,
    Parameter,
    FunctionPrototype,
    IfStatement,
    WhileStatement,
    ForStatement,
    FunctionCall,
    ReturnStatement,
    BreakStatement,
    ContinueStatement,
    Block,
    UnaryOperation,
    BinaryOperation,
    Assignment,
    ExpressionStatement,
    Identifier,
    Number,
)


class TestParser(unittest.TestCase):

    def parse_code(self, code):
        tokens = Lexer(code).tokenize()
        return Parser(tokens).parse()

    def test_function_definition(self):
        tree = self.parse_code(
            "int main(void) { return 0; }"
        )
        self.assertIsInstance(
            tree.declarations[0], Function
        )

    def test_variable_declaration(self):
        tree = self.parse_code(
            "int main(void) { int x = 10; return x; }"
        )
        statements = tree.declarations[0].body.statements
        self.assertEqual(statements[0].name, "x")

    def test_if_else_statement(self):
        tree = self.parse_code(
            "int main(void) { if (10 >= 5) return 1; else return 0; }"
        )
        statement = tree.declarations[0].body.statements[0]
        self.assertIsInstance(statement, IfStatement)

    def test_while_loop(self):
        tree = self.parse_code(
            "int main(void) { while (1 < 5) { return 0; } return 1; }"
        )
        statement = tree.declarations[0].body.statements[0]
        self.assertIsInstance(statement, WhileStatement)

    def test_for_loop(self):
        tree = self.parse_code(
            "int main(void) { int i; for (i = 0; i < 5; i = i + 1) { } return i; }"
        )
        statement = tree.declarations[0].body.statements[1]
        self.assertIsInstance(statement, ForStatement)

    def test_function_call(self):
        tree = self.parse_code(
            "int add(int a, int b) { return a + b; } "
            "int main(void) { return add(10, 20); }"
        )
        statement = tree.declarations[1].body.statements[0]
        self.assertIsInstance(statement, ReturnStatement)
        self.assertIsInstance(statement.expression, FunctionCall)

    def test_invalid_syntax(self):
        with self.assertRaises(SyntaxError):
            self.parse_code("int main(void) { return 0 }")

    def test_function_prototype(self):
        tree = self.parse_code(
            "int add(int a, int b); "
            "int main(void) { return add(10, 20); }"
        )
        self.assertIsInstance(
            tree.declarations[0], FunctionPrototype
        )

    def test_break_and_continue(self):
        tree = self.parse_code(
            "int main(void) { "
            "while (1) { "
            "if (1) break; else continue; "
            "} return 0; }"
        )
        loop = tree.declarations[0].body.statements[0]
        conditional = loop.body.statements[0]

        self.assertIsInstance(
            conditional.then_branch, BreakStatement
        )
        self.assertIsInstance(
            conditional.else_branch, ContinueStatement
        )

    def test_logical_operators(self):
        tree = self.parse_code(
            "int main(void) { "
            "int x = 10; "
            "if (x > 5 && x < 20 || !0) return 1; "
            "return 0; }"
        )
        condition = tree.declarations[0].body.statements[1].condition

        self.assertIsInstance(condition, BinaryOperation)
        self.assertEqual(condition.operator, "||")
        self.assertEqual(condition.left.operator, "&&")
        self.assertIsInstance(condition.right, UnaryOperation)

    def test_nested_blocks(self):
        tree = self.parse_code(
            "int main(void) { "
            "int x = 10; "
            "{ int y = 20; x = x + y; } "
            "return x; }"
        )
        nested_block = tree.declarations[0].body.statements[1]

        self.assertIsInstance(nested_block, Block)

    def test_unary_minus(self):
        tree = self.parse_code(
            "int main(void) { int x = -10; return -x; }"
        )
        statements = tree.declarations[0].body.statements

        self.assertIsInstance(
            statements[0].initializer, UnaryOperation
        )
        self.assertIsInstance(
            statements[1].expression, UnaryOperation
        )


    def test_operator_precedence(self):
        tree = self.parse_code(
            "int main(void) { return 1 + 2 * 3; }"
        )
        expression = tree.declarations[0].body.statements[0].expression

        self.assertEqual(expression.operator, "+")
        self.assertIsInstance(expression.right, BinaryOperation)
        self.assertEqual(expression.right.operator, "*")

    def test_parentheses_override_precedence(self):
        tree = self.parse_code(
            "int main(void) { return (1 + 2) * 3; }"
        )
        expression = tree.declarations[0].body.statements[0].expression

        self.assertEqual(expression.operator, "*")
        self.assertIsInstance(expression.left, BinaryOperation)
        self.assertEqual(expression.left.operator, "+")

    def test_assignment_expression_statement(self):
        tree = self.parse_code(
            "int main(void) { int x; x = 5; return x; }"
        )
        statement = tree.declarations[0].body.statements[1]

        self.assertIsInstance(statement, ExpressionStatement)
        self.assertIsInstance(statement.expression, Assignment)
        self.assertIsInstance(statement.expression.target, Identifier)
        self.assertIsInstance(statement.expression.value, Number)
        self.assertEqual(statement.expression.value.value, 5)

    def test_for_loop_with_declaration_initializer(self):
        tree = self.parse_code(
            "int main(void) { "
            "for (int i = 0; i < 3; i = i + 1) { } "
            "return 0; }"
        )
        loop = tree.declarations[0].body.statements[0]

        self.assertIsInstance(loop, ForStatement)
        self.assertEqual(loop.initializer.name, "i")
        self.assertIsInstance(loop.condition, BinaryOperation)
        self.assertIsInstance(loop.update, Assignment)


    def test_empty_parameter_list(self):
        tree = self.parse_code(
            "int main() { return 0; }"
        )
        function = tree.declarations[0]

        self.assertIsInstance(function, Function)
        self.assertEqual(function.parameters, [])

    def test_multiple_parameters_and_locations(self):
        tree = self.parse_code(
            "int add(int first, int second) { return first + second; }"
        )
        function = tree.declarations[0]

        self.assertEqual(len(function.parameters), 2)

        first, second = function.parameters

        self.assertIsInstance(first, Parameter)
        self.assertEqual(first.param_type, "int")
        self.assertEqual(first.name, "first")
        self.assertEqual(first.line, 1)
        self.assertIsNotNone(first.column)

        self.assertEqual(second.param_type, "int")
        self.assertEqual(second.name, "second")
        self.assertEqual(second.line, 1)
        self.assertIsNotNone(second.column)

    def test_multiple_function_call_arguments(self):
        tree = self.parse_code(
            "int add(int a, int b, int c) { return a + b + c; } "
            "int main(void) { return add(1, 2, 3); }"
        )
        call = tree.declarations[1].body.statements[0].expression

        self.assertIsInstance(call, FunctionCall)
        self.assertEqual(len(call.arguments), 3)
        self.assertEqual(
            [argument.value for argument in call.arguments],
            [1, 2, 3],
        )


if __name__ == "__main__":
    unittest.main()