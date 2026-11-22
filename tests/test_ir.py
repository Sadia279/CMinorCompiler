import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.ir import IRGenerator


class TestIRGenerator(unittest.TestCase):

    def generate_ir(self, code):
        tokens = Lexer(code).tokenize()
        tree = Parser(tokens).parse()
        return IRGenerator().generate(tree)

    def test_shadowed_variables_use_distinct_storage(self):
        code = """
        int main(void) {
            int x = 10;
            {
                int x = 20;
            }
            return x;
        }
        """

        ir = self.generate_ir(code)
        instructions = ir.functions[0].instructions

        stores = [
            instruction for instruction in instructions
            if instruction.opcode == "STORE"
        ]

        returns = [
            instruction for instruction in instructions
            if instruction.opcode == "RETURN"
        ]

        self.assertEqual(
            [instruction.result for instruction in stores],
            ["x__v1", "x__v2"]
        )
        self.assertEqual(returns[-1].operands, ["x__v1"])

    def test_assignment_updates_nearest_shadowed_variable(self):
        code = """
        int main(void) {
            int x = 10;
            {
                int x = 20;
                x = 30;
            }
            return x;
        }
        """

        ir = self.generate_ir(code)
        instructions = ir.functions[0].instructions

        stores = [
            instruction.result for instruction in instructions
            if instruction.opcode == "STORE"
        ]

        self.assertEqual(stores, ["x__v1", "x__v2", "x__v2"])

    def test_function_parameter_uses_internal_name(self):
        code = """
        int get(int value) {
            return value;
        }
        """

        ir = self.generate_ir(code)
        function = ir.functions[0]

        self.assertEqual(function.parameters, ["value__v1"])

        return_instruction = next(
            instruction for instruction in function.instructions
            if instruction.opcode == "RETURN"
        )

        self.assertEqual(
            return_instruction.operands,
            ["value__v1"]
        )

    def test_for_loop_variable_has_separate_scope(self):
        code = """
        int main(void) {
            int i = 9;
            for (int i = 0; i < 1; i = i + 1) {
            }
            return i;
        }
        """

        ir = self.generate_ir(code)
        instructions = ir.functions[0].instructions

        stores = [
            instruction.result for instruction in instructions
            if instruction.opcode == "STORE"
        ]

        returns = [
            instruction for instruction in instructions
            if instruction.opcode == "RETURN"
        ]

        self.assertEqual(stores, ["i__v1", "i__v2", "i__v2"])
        self.assertEqual(returns[-1].operands, ["i__v1"])

    def test_logical_and_uses_short_circuit_jump(self):
        code = """
        int main(void) {
            int a = 0;
            int b = 1;
            if (a && b) return 1;
            return 0;
        }
        """

        ir = self.generate_ir(code)
        opcodes = [
            instruction.opcode
            for instruction in ir.functions[0].instructions
        ]

        self.assertIn("IF_FALSE", opcodes)
        self.assertIn("LABEL", opcodes)

    def test_logical_or_uses_short_circuit_jump(self):
        code = """
        int main(void) {
            int a = 1;
            int b = 0;
            if (a || b) return 1;
            return 0;
        }
        """

        ir = self.generate_ir(code)
        opcodes = [
            instruction.opcode
            for instruction in ir.functions[0].instructions
        ]

        self.assertIn("IF_TRUE", opcodes)
        self.assertIn("LABEL", opcodes)


if __name__ == "__main__":
    unittest.main()
