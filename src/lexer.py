from dataclasses import dataclass


# Keywords supported by C Minor
KEYWORDS = {
    "int", "void", "if", "else",
    "while", "for", "break", "continue", "return"
}


# Token structure
@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def add_token(self, token):
        if len(self.tokens) >= 4000:
            raise SyntaxError(
                f"RESOURCE_LIMIT: Maximum 4000 tokens exceeded "
                f"at line {token.line}, column {token.column}"
            )
        self.tokens.append(token)

    def advance(self):
        char = self.source[self.position]

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1
        return char

    def tokenize(self):
        while self.position < len(self.source):
            char = self.source[self.position]

            # Ignore spaces, tabs and carriage returns
            if char in " \t\r":
                self.advance()
                continue

            # Ignore new lines
            if char == "\n":
                self.advance()
                continue

            # Reject preprocessor directives
            if char == "#":
                raise SyntaxError(
                    f"UNSUPPORTED_PREPROCESSING_DIRECTIVE: "
                    f"Preprocessor directives are not supported "
                    f"at line {self.line}, column {self.column}"
                )

            # Reject source line splicing
            if char == "\\" and self.source.startswith(
                "\\\n", self.position
            ):
                raise SyntaxError(
                    f"UNSUPPORTED_LINE_SPLICING: "
                    f"Source line splicing is not supported "
                    f"at line {self.line}, column {self.column}"
                )

            # Ignore single-line comments
            if self.source.startswith("//", self.position):
                while (self.position < len(self.source)
                       and self.source[self.position] != "\n"):
                    self.advance()
                continue

            # Ignore block comments
            if self.source.startswith("/*", self.position):
                start_line = self.line
                start_column = self.column

                self.advance()
                self.advance()

                while (self.position < len(self.source)
                       and not self.source.startswith("*/", self.position)):
                    self.advance()

                if self.position >= len(self.source):
                    raise SyntaxError(
                        f"Unterminated block comment at line "
                        f"{start_line}, column {start_column}"
                    )

                self.advance()
                self.advance()
                continue

            # Read decimal numbers
            if char.isdigit():
                start = self.position
                line = self.line
                column = self.column

                while (self.position < len(self.source)
                       and self.source[self.position].isdigit()):
                    self.advance()

                value = self.source[start:self.position]
                self.add_token(Token("NUMBER", value, line, column))
                continue

            # Read identifiers and keywords
            if char.isalpha() or char == "_":
                start = self.position
                line = self.line
                column = self.column

                while (self.position < len(self.source)
                       and (self.source[self.position].isalnum()
                            or self.source[self.position] == "_")):
                    self.advance()

                value = self.source[start:self.position]

                if value in KEYWORDS:
                    token_type = "KEYWORD"
                else:
                    token_type = "IDENTIFIER"

                self.add_token(
                    Token(token_type, value, line, column)
                )
                continue

            # Read two-character operators
            two_char = self.source[self.position:self.position + 2]

            if two_char in {"==", "!=", "<=", ">=", "&&", "||"}:
                self.add_token(
                    Token("OPERATOR", two_char, self.line, self.column)
                )
                self.advance()
                self.advance()
                continue

            # Read one-character operators
            if char in "+-*/%=<>!":
                self.add_token(
                    Token("OPERATOR", char, self.line, self.column)
                )
                self.advance()
                continue

            # Read symbols
            if char in ";,(){}":
                self.add_token(
                    Token("SYMBOL", char, self.line, self.column)
                )
                self.advance()
                continue

            raise SyntaxError(
                f"Unexpected character '{char}' "
                f"at line {self.line}, column {self.column}"
            )

        self.tokens.append(Token("EOF", "", self.line, self.column))
        return self.tokens
