
from dataclasses import dataclass, field

from src.lexer import Lexer


# ==========================================
# 1. ABSTRACT SYNTAX TREE (AST) NODES
# ==========================================

class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    declarations: list = field(default_factory=list)


@dataclass
class Parameter(ASTNode):
    param_type: str
    name: str
    line: int = None
    column: int = None


@dataclass
class Function(ASTNode):
    return_type: str
    name: str
    parameters: list
    body: object
    line: int = None
    column: int = None


@dataclass
class FunctionPrototype(ASTNode):
    return_type: str
    name: str
    parameters: list
    line: int = None
    column: int = None


@dataclass
class VariableDeclaration(ASTNode):
    var_type: str
    name: str
    initializer: object = None
    line: int = None
    column: int = None


@dataclass
class Block(ASTNode):
    statements: list = field(default_factory=list)


@dataclass
class ReturnStatement(ASTNode):
    expression: object = None


@dataclass
class IfStatement(ASTNode):
    condition: object
    then_branch: object
    else_branch: object = None


@dataclass
class WhileStatement(ASTNode):
    condition: object
    body: object


@dataclass
class ForStatement(ASTNode):
    initializer: object
    condition: object
    update: object
    body: object


@dataclass
class BreakStatement(ASTNode):
    pass


@dataclass
class ContinueStatement(ASTNode):
    pass


@dataclass
class ExpressionStatement(ASTNode):
    expression: object = None


@dataclass
class Number(ASTNode):
    value: int


@dataclass
class Identifier(ASTNode):
    name: str
    line: int = None
    column: int = None


@dataclass
class BinaryOperation(ASTNode):
    left: object
    operator: str
    right: object


@dataclass
class UnaryOperation(ASTNode):
    operator: str
    operand: object


@dataclass
class Assignment(ASTNode):
    target: object
    value: object


@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: list = field(default_factory=list)
    line: int = None
    column: int = None


# ==========================================
# 2. RECURSIVE-DESCENT PARSER
# ==========================================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.expression_depth = 0
        self.function_definition_count = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current_token()

        if token.type != "EOF":
            self.position += 1

        return token

    def check(self, value):
        return self.current_token().value == value

    def match(self, value):
        if self.check(value):
            self.advance()
            return True

        return False

    def expect(self, value):
        token = self.current_token()

        if token.value != value:
            raise SyntaxError(
                f"Expected '{value}' but found "
                f"'{token.value}' at line {token.line}, "
                f"column {token.column}"
            )

        return self.advance()

    def expect_identifier(self):
        token = self.current_token()

        if token.type != "IDENTIFIER":
            raise SyntaxError(
                f"Expected identifier at line {token.line}, "
                f"column {token.column}"
            )

        return self.advance().value


    def expect_identifier_token(self):
        token = self.current_token()

        if token.type != "IDENTIFIER":
            raise SyntaxError(
                f"Expected identifier at line {token.line}, "
                f"column {token.column}"
            )

        return self.advance()

    # ======================================
    # 3. PROGRAM AND FUNCTION PARSING
    # ======================================

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        declarations = []

        while self.current_token().type != "EOF":
            declarations.append(self.parse_function())

        self.expect("")

        return Program(declarations)

    def parse_function(self):
        return_type = self.parse_type()
        name_token = self.expect_identifier_token()
        name = name_token.value

        self.expect("(")
        parameters = self.parse_parameters()
        self.expect(")")

        if self.match(";"):
            return FunctionPrototype(
                return_type,
                name,
                parameters,
                name_token.line,
                name_token.column
            )

        self.function_definition_count += 1
        if self.function_definition_count > 32:
            raise SyntaxError(
                "RESOURCE_LIMIT: Maximum 32 user-defined function definitions exceeded"
            )

        body = self.parse_block()

        return Function(
            return_type,
            name,
            parameters,
            body,
            name_token.line,
            name_token.column
        )

    def parse_type(self):
        token = self.current_token()

        if token.value not in ("int", "void"):
            raise SyntaxError(
                f"Expected type at line {token.line}, "
                f"column {token.column}"
            )

        self.advance()
        return token.value

    def parse_parameters(self):
        parameters = []

        if self.check("void"):
            self.advance()
            return parameters

        if self.check(")"):
            return parameters

        while True:
            param_type = self.parse_type()

            if param_type == "void":
                token = self.current_token()
                raise SyntaxError(
                    f"void parameter must be the only parameter "
                    f"at line {token.line}, column {token.column}"
                )

            name_token = self.expect_identifier_token()

            parameters.append(
                Parameter(
                    param_type,
                    name_token.value,
                    name_token.line,
                    name_token.column
                )
            )

            if not self.match(","):
                break

        return parameters

    # ======================================
    # 4. STATEMENT PARSING
    # ======================================

    def parse_block(self):
        if not hasattr(self, "block_depth"):
            self.block_depth = 0

        self.block_depth += 1

        if self.block_depth > 16:
            self.block_depth -= 1
            token = self.current_token()
            raise SyntaxError(
                f"RESOURCE_LIMIT: Maximum 16 block nesting levels exceeded "
                f"at line {token.line}, column {token.column}"
            )

        try:
            self.expect("{")
            statements = []

            while not self.check("}"):
                if self.current_token().type == "EOF":
                    token = self.current_token()
                    raise SyntaxError(
                        f"Expected '}}' at line {token.line}, "
                        f"column {token.column}"
                    )

                statements.append(self.parse_statement())

            self.expect("}")
            return Block(statements)

        finally:
            self.block_depth -= 1

    def parse_statement(self):

        if self.check("{"):
            return self.parse_block()

        if self.check("int"):
            return self.parse_variable_declaration()

        if self.match("return"):
            expression = None

            if not self.check(";"):
                expression = self.parse_expression()

            self.expect(";")
            return ReturnStatement(expression)

        if self.match("if"):
            self.expect("(")
            condition = self.parse_expression()
            self.expect(")")

            then_branch = self.parse_statement()
            else_branch = None

            if self.match("else"):
                else_branch = self.parse_statement()

            return IfStatement(
                condition, then_branch, else_branch
            )

        if self.match("while"):
            self.expect("(")
            condition = self.parse_expression()
            self.expect(")")

            body = self.parse_statement()

            return WhileStatement(condition, body)

        if self.match("for"):
            self.expect("(")

            initializer = None

            if self.check("int"):
                initializer = self.parse_variable_declaration()
            elif not self.check(";"):
                initializer = self.parse_expression()
                self.expect(";")
            else:
                self.expect(";")

            condition = None

            if not self.check(";"):
                condition = self.parse_expression()

            self.expect(";")

            update = None

            if not self.check(")"):
                update = self.parse_expression()

            self.expect(")")

            body = self.parse_statement()

            return ForStatement(
                initializer, condition, update, body
            )

        if self.match("break"):
            self.expect(";")
            return BreakStatement()

        if self.match("continue"):
            self.expect(";")
            return ContinueStatement()

        if self.match(";"):
            return ExpressionStatement()

        expression = self.parse_expression()
        self.expect(";")

        return ExpressionStatement(expression)

    def parse_variable_declaration(self):
        var_type = self.parse_type()

        if var_type != "int":
            token = self.current_token()
            raise SyntaxError(
                f"Local variables must have type int "
                f"at line {token.line}, column {token.column}"
            )

        name_token = self.expect_identifier_token()
        initializer = None

        if self.match("="):
            initializer = self.parse_expression()

        self.expect(";")

        return VariableDeclaration(
            var_type,
            name_token.value,
            initializer,
            name_token.line,
            name_token.column
        )

    # ======================================
    # 5. EXPRESSION PARSING
    # ======================================

    def parse_expression(self):
        self.expression_depth += 1

        if self.expression_depth > 16:
            self.expression_depth -= 1
            raise SyntaxError(
                "RESOURCE_LIMIT: Maximum 16 expression nesting levels exceeded"
            )

        try:
            return self.parse_assignment()
        finally:
            self.expression_depth -= 1

    def parse_assignment(self):
        left = self.parse_logical_or()

        if self.match("="):
            value = self.parse_assignment()
            return Assignment(left, value)

        return left

    def parse_logical_or(self):
        expression = self.parse_logical_and()

        while self.match("||"):
            operator = "||"
            right = self.parse_logical_and()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_logical_and(self):
        expression = self.parse_equality()

        while self.match("&&"):
            operator = "&&"
            right = self.parse_equality()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_equality(self):
        expression = self.parse_relational()

        while self.check("==") or self.check("!="):
            operator = self.advance().value
            right = self.parse_relational()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_relational(self):
        expression = self.parse_additive()

        while (
            self.check("<")
            or self.check(">")
            or self.check("<=")
            or self.check(">=")
        ):
            operator = self.advance().value
            right = self.parse_additive()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_additive(self):
        expression = self.parse_multiplicative()

        while self.check("+") or self.check("-"):
            operator = self.advance().value
            right = self.parse_multiplicative()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_multiplicative(self):
        expression = self.parse_unary()

        while (
            self.check("*")
            or self.check("/")
            or self.check("%")
        ):
            operator = self.advance().value
            right = self.parse_unary()

            expression = BinaryOperation(
                expression, operator, right
            )

        return expression

    def parse_unary(self):
        if self.check("!") or self.check("-") or self.check("+"):
            operator = self.advance().value
            operand = self.parse_unary()

            return UnaryOperation(operator, operand)

        return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()

        if token.type == "NUMBER":
            self.advance()
            return Number(int(token.value))

        if token.type == "IDENTIFIER":
            name_token = self.advance()
            name = name_token.value

            if self.match("("):
                arguments = []

                if not self.check(")"):
                    while True:
                        arguments.append(
                            self.parse_expression()
                        )

                        if not self.match(","):
                            break

                self.expect(")")

                return FunctionCall(
                    name,
                    arguments,
                    name_token.line,
                    name_token.column
                )

            return Identifier(
                name,
                name_token.line,
                name_token.column
            )

        if self.match("("):
            expression = self.parse_expression()
            self.expect(")")
            return expression

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}"
        )
