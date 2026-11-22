import unittest

from src.lexer import Lexer


class TestLexer(unittest.TestCase):

    def test_keywords_and_identifiers(self):
        tokens = Lexer("int age = 20;").tokenize()

        self.assertEqual(tokens[0].value, "int")
        self.assertEqual(tokens[0].type, "KEYWORD")
        self.assertEqual(tokens[1].value, "age")
        self.assertEqual(tokens[1].type, "IDENTIFIER")

    def test_numbers_and_operators(self):
        tokens = Lexer("int x = 10 + 20;").tokenize()

        values = [token.value for token in tokens]

        self.assertEqual(
            values,
            ["int", "x", "=", "10", "+", "20", ";", ""]
        )

    def test_logical_operators(self):
        tokens = Lexer("int x = 10 && 5 || !0;").tokenize()

        operators = [
            token.value for token in tokens
            if token.type == "OPERATOR"
        ]

        self.assertEqual(operators, ["=", "&&", "||", "!"])

    def test_comparison_operators(self):
        tokens = Lexer("10 >= 5 <= 20 == 20 != 0").tokenize()

        operators = [
            token.value for token in tokens
            if token.type == "OPERATOR"
        ]

        self.assertEqual(
            operators,
            [">=", "<=", "==", "!="]
        )

    def test_comments_are_ignored(self):
        tokens = Lexer("int x = 10; // comment").tokenize()

        values = [token.value for token in tokens]

        self.assertNotIn("//", values)
        self.assertNotIn("comment", values)

    def test_block_comments_are_ignored(self):
        tokens = Lexer(
            "int x = 10; /* block comment */ return x;"
        ).tokenize()

        values = [token.value for token in tokens]

        self.assertNotIn("block", values)
        self.assertNotIn("comment", values)
        self.assertIn("return", values)

    def test_block_comment_between_identifiers(self):
        tokens = Lexer("int/**/b = 5;").tokenize()

        values = [token.value for token in tokens]

        self.assertEqual(
            values,
            ["int", "b", "=", "5", ";", ""]
        )

    def test_unterminated_block_comment(self):
        with self.assertRaisesRegex(
            SyntaxError, "Unterminated block comment"
        ):
            Lexer("int x = 10; /* unfinished").tokenize()

    def test_invalid_character(self):
        with self.assertRaises(SyntaxError):
            Lexer("int x = 10 @ 5;").tokenize()

    def test_line_and_column_tracking(self):
        tokens = Lexer("int x;\nreturn 5;").tokenize()

        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[0].column, 1)

        return_token = next(
            token for token in tokens
            if token.value == "return"
        )

        self.assertEqual(return_token.line, 2)
        self.assertEqual(return_token.column, 1)


    def test_all_arithmetic_operators(self):
        tokens = Lexer("a + b - c * d / e % f").tokenize()
        operators = [
            token.value for token in tokens
            if token.type == "OPERATOR"
        ]

        self.assertEqual(operators, ["+", "-", "*", "/", "%"])

    def test_all_punctuation_and_delimiters(self):
        tokens = Lexer("( ) { } , ;").tokenize()
        symbols = [
            token.value for token in tokens
            if token.type == "SYMBOL"
        ]

        self.assertEqual(symbols, ["(", ")", "{", "}", ",", ";"])

    def test_whitespace_and_newline_handling(self):
        tokens = Lexer("int\tvalue = 10;\nreturn\tvalue;").tokenize()
        values = [token.value for token in tokens]

        self.assertEqual(
            values,
            ["int", "value", "=", "10", ";", "return", "value", ";", ""]
        )

        return_token = next(
            token for token in tokens if token.value == "return"
        )
        self.assertEqual(return_token.line, 2)
        self.assertEqual(return_token.column, 1)

    def test_keyword_and_identifier_boundaries(self):
        tokens = Lexer("int int1 integer _int int_value").tokenize()

        self.assertEqual(
            [(token.type, token.value) for token in tokens[:-1]],
            [
                ("KEYWORD", "int"),
                ("IDENTIFIER", "int1"),
                ("IDENTIFIER", "integer"),
                ("IDENTIFIER", "_int"),
                ("IDENTIFIER", "int_value"),
            ],
        )

    def test_invalid_character_reports_location(self):
        with self.assertRaisesRegex(
            SyntaxError,
            r"Unexpected character '@' at line 2, column 2",
        ):
            Lexer("int x;\n @").tokenize()



    def test_preprocessor_directive_is_rejected(self):
        with self.assertRaisesRegex(
            SyntaxError, "UNSUPPORTED_PREPROCESSING_DIRECTIVE"
        ):
            Lexer("#include <stdio.h>").tokenize()

    def test_line_splicing_is_rejected(self):
        source = "int x = 1 + " + chr(92) + "\n2;"
        with self.assertRaisesRegex(
            SyntaxError, "UNSUPPORTED_LINE_SPLICING"
        ):
            Lexer(source).tokenize()

    def test_directive_inside_block_comment_is_accepted(self):
        tokens = Lexer(
            "/* #include <stdio.h> */ int main(void) { return 0; }"
        ).tokenize()
        self.assertEqual(tokens[0].value, "int")

    def test_directive_inside_line_comment_is_accepted(self):
        tokens = Lexer(
            "// #include <stdio.h>\nint main(void) { return 0; }"
        ).tokenize()
        self.assertEqual(tokens[0].value, "int")


if __name__ == "__main__":
    unittest.main()
