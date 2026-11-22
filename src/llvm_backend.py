from src.ir import IRProgram


class LLVMBackend:

    def __init__(self):
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"%v{self.temp_count}"

    def generate(self, program):

        if not isinstance(program, IRProgram):
            raise TypeError("Expected an IRProgram")

        output = [
            'target triple = "x86_64-pc-linux-gnu"',
            ""
        ]

        for function in program.functions:
            output.extend(self.generate_function(function))

        return "\n".join(output)

    def generate_function(self, function):

        self.temp_count = 0

        instructions = function.instructions

        # Find all variables and temporary values.
        variables = set(function.parameters)

        for instruction in instructions:

            op = instruction.opcode
            operands = instruction.operands

            if op == "STORE":
                variables.add(instruction.result)
                self.add_value(variables, operands[0])

            elif op.startswith("BINARY_"):
                variables.add(instruction.result)
                self.add_value(variables, operands[0])
                self.add_value(variables, operands[1])

            elif op.startswith("UNARY_"):
                variables.add(instruction.result)
                self.add_value(variables, operands[0])

            elif op == "CALL":
                if instruction.result:
                    variables.add(instruction.result)

                for argument in operands[1:]:
                    self.add_value(variables, argument)

            elif op in ("RETURN", "IF_FALSE", "IF_TRUE"):
                if operands:
                    self.add_value(variables, operands[0])

        # Map IR labels to LLVM basic blocks.
        labels = {}

        for index, instruction in enumerate(instructions):
            if instruction.opcode == "LABEL":
                labels[instruction.operands[0]] = f"bb{index}"

        # Function signature.
        parameters = ", ".join(
            f"i32 %arg{i}"
            for i in range(len(function.parameters))
        )

        return_type = "i32" if function.return_type == "int" else "void"

        output = [
            f"define {return_type} @{function.name}({parameters}) {{",
            "entry:"
        ]

        # Allocate storage for variables and temporaries.
        for variable in sorted(variables):
            output.append(f"    %slot.{variable} = alloca i32")

        # Store function parameters.
        for index, parameter in enumerate(function.parameters):
            output.append(
                f"    store i32 %arg{index}, ptr %slot.{parameter}"
            )

        if instructions:
            output.append("    br label %bb0")

        # Generate one LLVM basic block per IR instruction.
        for index, instruction in enumerate(instructions):

            op = instruction.opcode
            operands = instruction.operands
            next_block = f"bb{index + 1}"

            output.append("")
            output.append(f"bb{index}:")

            if op == "LABEL":
                output.append(f"    br label %{next_block}")

            elif op == "STORE":
                value = self.get_value(operands[0], output)

                output.append(
                    f"    store i32 {value}, ptr %slot.{instruction.result}"
                )

                output.append(f"    br label %{next_block}")

            elif op.startswith("BINARY_"):
                self.generate_binary(
                    instruction, output, next_block
                )

            elif op.startswith("UNARY_"):
                self.generate_unary(
                    instruction, output, next_block
                )

            elif op == "CALL":
                self.generate_call(
                    instruction, output, next_block
                )

            elif op == "IF_FALSE":
                condition = self.get_value(operands[0], output)
                target = labels[operands[1]]

                condition_temp = self.new_temp()

                output.append(
                    f"    {condition_temp} = icmp ne i32 {condition}, 0"
                )

                output.append(
                    f"    br i1 {condition_temp}, "
                    f"label %{next_block}, label %{target}"
                )

            elif op == "IF_TRUE":
                condition = self.get_value(operands[0], output)
                target = labels[operands[1]]

                condition_temp = self.new_temp()

                output.append(
                    f"    {condition_temp} = icmp ne i32 {condition}, 0"
                )

                output.append(
                    f"    br i1 {condition_temp}, "
                    f"label %{target}, label %{next_block}"
                )

            elif op == "GOTO":
                target = labels[operands[0]]
                output.append(f"    br label %{target}")

            elif op == "RETURN":

                if operands:
                    value = self.get_value(operands[0], output)
                    output.append(f"    ret i32 {value}")
                else:
                    output.append("    ret void")

            elif op == "END_FUNCTION":

                if function.return_type == "void":
                    output.append("    ret void")
                else:
                    output.append("    unreachable")

            else:
                raise ValueError(f"Unsupported IR instruction: {op}")

        output.append("}")
        output.append("")

        return output

    def add_value(self, variables, value):

        if value is None:
            return

        try:
            int(value)
        except ValueError:
            variables.add(value)

    def get_value(self, value, output):

        try:
            int(value)
            return value
        except ValueError:
            temp = self.new_temp()

            output.append(
                f"    {temp} = load i32, ptr %slot.{value}"
            )

            return temp

    def generate_binary(self, instruction, output, next_block):

        operator = instruction.opcode.replace("BINARY_", "")

        left = self.get_value(instruction.operands[0], output)
        right = self.get_value(instruction.operands[1], output)

        result = instruction.result

        arithmetic = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "sdiv",
            "%": "srem"
        }

        comparisons = {
            "==": "eq",
            "!=": "ne",
            "<": "slt",
            "<=": "sle",
            ">": "sgt",
            ">=": "sge"
        }

        if operator in arithmetic:

            temp = self.new_temp()

            output.append(
                f"    {temp} = {arithmetic[operator]} "
                f"i32 {left}, {right}"
            )

            output.append(
                f"    store i32 {temp}, ptr %slot.{result}"
            )

        elif operator in comparisons:

            comparison = self.new_temp()
            temp = self.new_temp()

            output.append(
                f"    {comparison} = icmp {comparisons[operator]} "
                f"i32 {left}, {right}"
            )

            output.append(
                f"    {temp} = zext i1 {comparison} to i32"
            )

            output.append(
                f"    store i32 {temp}, ptr %slot.{result}"
            )

        else:
            raise ValueError(f"Unsupported binary operator: {operator}")

        output.append(f"    br label %{next_block}")

    def generate_unary(self, instruction, output, next_block):

        operator = instruction.opcode.replace("UNARY_", "")

        operand = self.get_value(instruction.operands[0], output)
        result = instruction.result

        temp = self.new_temp()

        if operator == "-":

            output.append(
                f"    {temp} = sub i32 0, {operand}"
            )

        elif operator == "!":

            comparison = self.new_temp()

            output.append(
                f"    {comparison} = icmp eq i32 {operand}, 0"
            )

            output.append(
                f"    {temp} = zext i1 {comparison} to i32"
            )

        elif operator == "+":

            output.append(
                f"    {temp} = add i32 0, {operand}"
            )

        else:
            raise ValueError(f"Unsupported unary operator: {operator}")

        output.append(
            f"    store i32 {temp}, ptr %slot.{result}"
        )

        output.append(f"    br label %{next_block}")

    def generate_call(self, instruction, output, next_block):

        operands = instruction.operands

        function_name = operands[0]

        arguments = []

        for argument in operands[1:]:
            value = self.get_value(argument, output)
            arguments.append(f"i32 {value}")

        argument_text = ", ".join(arguments)

        if instruction.result is not None:

            temp = self.new_temp()

            output.append(
                f"    {temp} = call i32 @{function_name}({argument_text})"
            )

            output.append(
                f"    store i32 {temp}, ptr %slot.{instruction.result}"
            )

        else:

            output.append(
                f"    call void @{function_name}({argument_text})"
            )

        output.append(f"    br label %{next_block}")
