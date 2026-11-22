
from dataclasses import dataclass, field

from src.parser import (
    Program,
    Function,
    VariableDeclaration,
    Block,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    BreakStatement,
    ContinueStatement,
    ExpressionStatement,
    Number,
    Identifier,
    BinaryOperation,
    UnaryOperation,
    Assignment,
    FunctionCall,
)


# ==========================================
# 1. IR DATA STRUCTURES
# ==========================================

@dataclass
class IRInstruction:
    opcode: str
    operands: list = field(default_factory=list)
    result: str = None


@dataclass
class IRFunction:
    name: str
    return_type: str
    parameters: list = field(default_factory=list)
    instructions: list = field(default_factory=list)


@dataclass
class IRProgram:
    functions: list = field(default_factory=list)


# ==========================================
# 2. IR GENERATOR
# ==========================================

class IRGenerator:

    def __init__(self):
        self.program = None
        self.current_function = None
        self.temp_count = 0
        self.label_count = 0
        self.loop_stack = []
        self.function_return_types = {}
        self.variable_scopes = []
        self.variable_count = 0

    # ======================================
    # TEMPORARY AND LABEL GENERATION
    # ======================================

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self, prefix="L"):
        self.label_count += 1
        return f"{prefix}{self.label_count}"

    # ======================================
    # VARIABLE SCOPE MANAGEMENT
    # ======================================

    def enter_variable_scope(self):
        self.variable_scopes.append({})

    def exit_variable_scope(self):
        if self.variable_scopes:
            self.variable_scopes.pop()

    def declare_variable(self, name):
        if not self.variable_scopes:
            self.enter_variable_scope()

        self.variable_count += 1
        internal_name = f"{name}__v{self.variable_count}"
        self.variable_scopes[-1][name] = internal_name
        return internal_name

    def resolve_variable(self, name):
        for scope in reversed(self.variable_scopes):
            if name in scope:
                return scope[name]

        raise ValueError(
            f"IR generation encountered undeclared variable '{name}'"
        )

    # ======================================
    # EMIT IR INSTRUCTION
    # ======================================

    def emit(self, opcode, operands=None, result=None):

        instruction = IRInstruction(
            opcode,
            operands if operands is not None else [],
            result
        )

        self.current_function.instructions.append(
            instruction
        )

    # ======================================
    # PROGRAM GENERATION
    # ======================================

    def generate(self, program):

        if not isinstance(program, Program):
            raise TypeError("Expected a Program AST")

        self.program = IRProgram()
        self.temp_count = 0
        self.label_count = 0
        self.function_return_types = {}

        # Collect function return types.
        for declaration in program.declarations:

            self.function_return_types[declaration.name] = (
                declaration.return_type
            )

        # Generate IR for function definitions.
        for declaration in program.declarations:

            if isinstance(declaration, Function):
                self.generate_function(declaration)

        return self.program

    # ======================================
    # FUNCTION GENERATION
    # ======================================

    def generate_function(self, function):

        self.current_function = IRFunction(
            function.name,
            function.return_type,
            [
                parameter.name
                for parameter in function.parameters
            ]
        )

        self.loop_stack = []
        self.variable_scopes = []
        self.enter_variable_scope()

        for parameter in function.parameters:
            self.declare_variable(parameter.name)

        self.current_function.parameters = [
            self.resolve_variable(parameter.name)
            for parameter in function.parameters
        ]

        self.generate_block(function.body, create_scope=False)

        self.emit("END_FUNCTION")
        self.exit_variable_scope()

        self.program.functions.append(
            self.current_function
        )

    # ======================================
    # BLOCK GENERATION
    # ======================================

    def generate_block(self, block, create_scope=True):

        if create_scope:
            self.enter_variable_scope()

        try:
            for statement in block.statements:
                self.generate_statement(statement)
        finally:
            if create_scope:
                self.exit_variable_scope()

    # ======================================
    # STATEMENT GENERATION
    # ======================================

    def generate_statement(self, statement):

        # Nested block
        if isinstance(statement, Block):

            self.generate_block(statement)

        # Variable declaration
        elif isinstance(statement, VariableDeclaration):

            internal_name = self.declare_variable(statement.name)

            if statement.initializer is not None:

                value = self.generate_expression(
                    statement.initializer
                )

                self.emit(
                    "STORE",
                    [value],
                    internal_name
                )

        # Return statement
        elif isinstance(statement, ReturnStatement):

            if statement.expression is None:
                self.emit("RETURN")

            else:

                value = self.generate_expression(
                    statement.expression
                )

                self.emit("RETURN", [value])

        # Expression statement
        elif isinstance(statement, ExpressionStatement):

            if statement.expression is not None:

                self.generate_expression(
                    statement.expression
                )

        # If / Else
        elif isinstance(statement, IfStatement):

            else_label = self.new_label("else")
            end_label = self.new_label("endif")

            condition = self.generate_expression(
                statement.condition
            )

            self.emit(
                "IF_FALSE",
                [condition, else_label]
            )

            self.generate_statement(
                statement.then_branch
            )

            self.emit("GOTO", [end_label])
            self.emit("LABEL", [else_label])

            if statement.else_branch is not None:

                self.generate_statement(
                    statement.else_branch
                )

            self.emit("LABEL", [end_label])

        # While loop
        elif isinstance(statement, WhileStatement):

            start_label = self.new_label("while")
            end_label = self.new_label("endwhile")

            self.emit("LABEL", [start_label])

            condition = self.generate_expression(
                statement.condition
            )

            self.emit(
                "IF_FALSE",
                [condition, end_label]
            )

            self.loop_stack.append(
                (start_label, end_label)
            )

            self.generate_statement(statement.body)

            self.loop_stack.pop()

            self.emit("GOTO", [start_label])
            self.emit("LABEL", [end_label])

        # For loop
        elif isinstance(statement, ForStatement):

            self.enter_variable_scope()
            try:
                start_label = self.new_label("for")
                update_label = self.new_label("update")
                end_label = self.new_label("endfor")

                # Initialization
                if statement.initializer is not None:

                    if isinstance(
                        statement.initializer,
                        VariableDeclaration
                    ):

                        self.generate_statement(
                            statement.initializer
                        )

                    else:

                        self.generate_expression(
                            statement.initializer
                        )

                self.emit("LABEL", [start_label])

                # Condition
                if statement.condition is not None:

                    condition = self.generate_expression(
                        statement.condition
                    )

                    self.emit(
                        "IF_FALSE",
                        [condition, end_label]
                    )

                self.loop_stack.append(
                    (update_label, end_label)
                )

                self.generate_statement(statement.body)

                self.loop_stack.pop()

                # Update
                self.emit("LABEL", [update_label])

                if statement.update is not None:

                    self.generate_expression(
                        statement.update
                    )

                self.emit("GOTO", [start_label])
                self.emit("LABEL", [end_label])
            finally:
                self.exit_variable_scope()

        # Break
        elif isinstance(statement, BreakStatement):

            if self.loop_stack:

                break_label = self.loop_stack[-1][1]

                self.emit("GOTO", [break_label])

        # Continue
        elif isinstance(statement, ContinueStatement):

            if self.loop_stack:

                continue_label = self.loop_stack[-1][0]

                self.emit("GOTO", [continue_label])

        else:

            raise TypeError(
                f"Unsupported statement: "
                f"{type(statement).__name__}"
            )

    # ======================================
    # EXPRESSION GENERATION
    # ======================================

    def generate_expression(self, expression):

        # Integer constant
        if isinstance(expression, Number):

            return str(expression.value)

        # Variable
        if isinstance(expression, Identifier):

            return self.resolve_variable(expression.name)

        # Unary operation
        if isinstance(expression, UnaryOperation):

            operand = self.generate_expression(
                expression.operand
            )

            result = self.new_temp()

            self.emit(
                "UNARY_" + expression.operator,
                [operand],
                result
            )

            return result

        # Binary operation
        if isinstance(expression, BinaryOperation):

            # Short-circuit logical AND and OR
            if expression.operator == "&&":
                return self.generate_logical_and(expression)

            if expression.operator == "||":
                return self.generate_logical_or(expression)

            left = self.generate_expression(
                expression.left
            )

            right = self.generate_expression(
                expression.right
            )

            result = self.new_temp()

            self.emit(
                "BINARY_" + expression.operator,
                [left, right],
                result
            )

            return result

        # Assignment
        if isinstance(expression, Assignment):

            value = self.generate_expression(
                expression.value
            )

            target_name = self.resolve_variable(
                expression.target.name
            )

            self.emit(
                "STORE",
                [value],
                target_name
            )

            return target_name

        # Function call
        if isinstance(expression, FunctionCall):

            arguments = []

            for argument in expression.arguments:

                arguments.append(
                    self.generate_expression(argument)
                )

            return_type = self.function_return_types.get(
                expression.name
            )

            if return_type == "void":

                self.emit(
                    "CALL",
                    [expression.name] + arguments
                )

                return None

            result = self.new_temp()

            self.emit(
                "CALL",
                [expression.name] + arguments,
                result
            )

            return result

        raise TypeError(
            f"Unsupported expression: "
            f"{type(expression).__name__}"
        )

    # ======================================
    # LOGICAL AND: SHORT-CIRCUIT
    # ======================================

    def generate_logical_and(self, expression):

        result = self.new_temp()

        false_label = self.new_label("and_false")
        end_label = self.new_label("and_end")

        left = self.generate_expression(
            expression.left
        )

        self.emit(
            "IF_FALSE",
            [left, false_label]
        )

        right = self.generate_expression(
            expression.right
        )

        self.emit(
            "IF_FALSE",
            [right, false_label]
        )

        self.emit("STORE", ["1"], result)

        self.emit("GOTO", [end_label])

        self.emit("LABEL", [false_label])

        self.emit("STORE", ["0"], result)

        self.emit("LABEL", [end_label])

        return result

    # ======================================
    # LOGICAL OR: SHORT-CIRCUIT
    # ======================================

    def generate_logical_or(self, expression):

        result = self.new_temp()

        true_label = self.new_label("or_true")
        end_label = self.new_label("or_end")

        left = self.generate_expression(
            expression.left
        )

        self.emit(
            "IF_TRUE",
            [left, true_label]
        )

        right = self.generate_expression(
            expression.right
        )

        self.emit(
            "IF_TRUE",
            [right, true_label]
        )

        self.emit("STORE", ["0"], result)

        self.emit("GOTO", [end_label])

        self.emit("LABEL", [true_label])

        self.emit("STORE", ["1"], result)

        self.emit("LABEL", [end_label])

        return result


# ==========================================
# 3. IR PRINTER
# ==========================================

def print_ir(program):

    for function in program.functions:

        print(f"\nFUNCTION {function.name}")
        print(f"RETURN_TYPE {function.return_type}")
        print(
            f"PARAMETERS {', '.join(function.parameters)}"
        )

        for instruction in function.instructions:

            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "LABEL":

                print(f"{operands[0]}:")

            elif opcode == "STORE":

                print(
                    f"    {instruction.result} = "
                    f"{operands[0]}"
                )

            elif opcode.startswith("BINARY_"):

                operator = opcode.replace("BINARY_", "")

                left, right = operands

                print(
                    f"    {instruction.result} = "
                    f"{left} {operator} {right}"
                )

            elif opcode.startswith("UNARY_"):

                operator = opcode.replace("UNARY_", "")

                print(
                    f"    {instruction.result} = "
                    f"{operator}{operands[0]}"
                )

            elif opcode == "RETURN":

                if operands:
                    print(f"    RETURN {operands[0]}")
                else:
                    print("    RETURN")

            elif opcode == "GOTO":

                print(f"    GOTO {operands[0]}")

            elif opcode == "IF_FALSE":

                print(
                    f"    IF_FALSE {operands[0]} "
                    f"GOTO {operands[1]}"
                )

            elif opcode == "IF_TRUE":

                print(
                    f"    IF_TRUE {operands[0]} "
                    f"GOTO {operands[1]}"
                )

            elif opcode == "CALL":

                name = operands[0]
                arguments = ", ".join(operands[1:])

                if instruction.result is not None:

                    print(
                        f"    {instruction.result} = "
                        f"CALL {name}({arguments})"
                    )

                else:

                    print(
                        f"    CALL {name}({arguments})"
                    )

            elif opcode == "END_FUNCTION":

                print("END_FUNCTION")

            else:

                print(
                    f"    {opcode} {operands}"
                )
