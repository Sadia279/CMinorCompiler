
import unittest

from src.ir import IRInstruction, IRFunction, IRProgram
from src.llvm_backend import LLVMBackend


class TestLLVMBackend(unittest.TestCase):

    def setUp(self):
        self.backend = LLVMBackend()

    def make_program(self, instructions, return_type="int",
                     parameters=None):
        function = IRFunction(
            name="main",
            return_type=return_type,
            parameters=parameters or [],
            instructions=instructions
        )
        return IRProgram(functions=[function])

    def test_rejects_non_ir_program(self):
        with self.assertRaises(TypeError):
            self.backend.generate("invalid")

    def test_generates_target_triple(self):
        program = self.make_program([
            IRInstruction("RETURN", ["0"])
        ])
        result = self.backend.generate(program)

        self.assertIn(
            'target triple = "x86_64-pc-linux-gnu"',
            result
        )

    def test_generates_integer_function(self):
        program = self.make_program([
            IRInstruction("RETURN", ["10"])
        ])
        result = self.backend.generate(program)

        self.assertIn("define i32 @main()", result)
        self.assertIn("ret i32 10", result)

    def test_allocates_parameter_slots(self):
        program = self.make_program(
            [
                IRInstruction("RETURN", ["a"])
            ],
            parameters=["a"]
        )
        result = self.backend.generate(program)

        self.assertIn("%slot.a = alloca i32", result)
        self.assertIn("store i32 %arg0", result)

    def test_generates_addition(self):
        program = self.make_program([
            IRInstruction("BINARY_+", ["7", "3"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("add i32 7, 3", result)

    def test_generates_subtraction(self):
        program = self.make_program([
            IRInstruction("BINARY_-", ["7", "3"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("sub i32 7, 3", result)

    def test_generates_multiplication(self):
        program = self.make_program([
            IRInstruction("BINARY_*", ["7", "3"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("mul i32 7, 3", result)

    def test_generates_signed_division(self):
        program = self.make_program([
            IRInstruction("BINARY_/", ["10", "2"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("sdiv i32 10, 2", result)

    def test_generates_signed_remainder(self):
        program = self.make_program([
            IRInstruction("BINARY_%", ["10", "3"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("srem i32 10, 3", result)

    def test_generates_equality_comparison(self):
        program = self.make_program([
            IRInstruction("BINARY_==", ["5", "5"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("icmp eq i32 5, 5", result)
        self.assertIn("zext i1", result)

    def test_generates_remaining_comparisons(self):
        comparisons = [
            ("!=", "ne"),
            ("<", "slt"),
            ("<=", "sle"),
            (">", "sgt"),
            (">=", "sge"),
        ]

        for operator, llvm_operator in comparisons:
            with self.subTest(operator=operator):
                program = self.make_program([
                    IRInstruction(
                        f"BINARY_{operator}",
                        ["5", "3"],
                        "t1"
                    ),
                    IRInstruction("RETURN", ["t1"])
                ])

                result = self.backend.generate(program)

                self.assertIn(
                    f"icmp {llvm_operator} i32 5, 3",
                    result
                )
                self.assertIn("zext i1", result)

    def test_generates_unary_minus(self):
        program = self.make_program([
            IRInstruction("UNARY_-", ["5"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("sub i32 0, 5", result)

    def test_generates_unary_plus(self):
        program = self.make_program([
            IRInstruction("UNARY_+", ["5"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("add i32 0, 5", result)

    def test_generates_logical_not(self):
        program = self.make_program([
            IRInstruction("UNARY_!", ["0"], "t1"),
            IRInstruction("RETURN", ["t1"])
        ])
        result = self.backend.generate(program)

        self.assertIn("icmp eq i32 0, 0", result)
        self.assertIn("zext i1", result)

    def test_generates_function_call(self):
        program = IRProgram(functions=[
            IRFunction(
                "add",
                "int",
                ["a", "b"],
                [
                    IRInstruction("BINARY_+", ["a", "b"], "t1"),
                    IRInstruction("RETURN", ["t1"])
                ]
            ),
            IRFunction(
                "main",
                "int",
                [],
                [
                    IRInstruction("CALL", ["add", "2", "3"], "t2"),
                    IRInstruction("RETURN", ["t2"])
                ]
            )
        ])

        result = self.backend.generate(program)

        self.assertIn(
            "call i32 @add(i32 2, i32 3)",
            result
        )

    def test_generates_conditional_branch(self):
        program = self.make_program([
            IRInstruction("IF_FALSE", ["1", "L1"]),
            IRInstruction("GOTO", ["L1"]),
            IRInstruction("LABEL", ["L1"]),
            IRInstruction("RETURN", ["0"])
        ])
        result = self.backend.generate(program)

        self.assertIn("icmp ne i32 1, 0", result)
        self.assertIn("br i1", result)
        self.assertIn("label %bb2", result)

    def test_generates_if_true_branch(self):
        program = self.make_program([
            IRInstruction("IF_TRUE", ["1", "L1"]),
            IRInstruction("RETURN", ["0"]),
            IRInstruction("LABEL", ["L1"]),
            IRInstruction("RETURN", ["1"])
        ])

        result = self.backend.generate(program)

        self.assertIn("icmp ne i32 1, 0", result)
        self.assertIn("br i1", result)
        self.assertIn("label %bb2", result)

    def test_generates_void_function(self):
        program = self.make_program(
            [
                IRInstruction("RETURN")
            ],
            return_type="void"
        )
        result = self.backend.generate(program)

        self.assertIn("define void @main()", result)
        self.assertIn("ret void", result)

    def test_rejects_unsupported_instruction(self):
        program = self.make_program([
            IRInstruction("UNKNOWN")
        ])

        with self.assertRaises(ValueError):
            self.backend.generate(program)


    def test_generates_store_and_load(self):
        program = self.make_program([
            IRInstruction("STORE", ["7"], "x"),
            IRInstruction("RETURN", ["x"])
        ])

        result = self.backend.generate(program)

        self.assertIn("%slot.x = alloca i32", result)
        self.assertIn("store i32 7, ptr %slot.x", result)
        self.assertIn("load i32, ptr %slot.x", result)

    def test_loads_function_parameter(self):
        program = self.make_program(
            [IRInstruction("RETURN", ["a"])],
            parameters=["a"]
        )

        result = self.backend.generate(program)

        self.assertIn("load i32, ptr %slot.a", result)

    def test_generates_void_function_call(self):
        program = IRProgram(functions=[
            IRFunction(
                "notify",
                "void",
                [],
                [IRInstruction("RETURN")]
            ),
            IRFunction(
                "main",
                "int",
                [],
                [
                    IRInstruction("CALL", ["notify"]),
                    IRInstruction("RETURN", ["0"])
                ]
            )
        ])

        result = self.backend.generate(program)

        self.assertIn("call void @notify()", result)

    def test_generates_zero_argument_function_call(self):
        program = IRProgram(functions=[
            IRFunction(
                "answer",
                "int",
                [],
                [IRInstruction("RETURN", ["42"])]
            ),
            IRFunction(
                "main",
                "int",
                [],
                [
                    IRInstruction("CALL", ["answer"], "t1"),
                    IRInstruction("RETURN", ["t1"])
                ]
            )
        ])

        result = self.backend.generate(program)

        self.assertIn("call i32 @answer()", result)

    def test_generates_unconditional_goto(self):
        program = self.make_program([
            IRInstruction("GOTO", ["L1"]),
            IRInstruction("RETURN", ["0"]),
            IRInstruction("LABEL", ["L1"]),
            IRInstruction("RETURN", ["1"])
        ])

        result = self.backend.generate(program)

        self.assertIn("br label %bb2", result)

    def test_generates_end_function(self):
        cases = [
            ("int", "unreachable"),
            ("void", "ret void")
        ]

        for return_type, expected in cases:
            with self.subTest(return_type=return_type):
                program = self.make_program(
                    [IRInstruction("END_FUNCTION")],
                    return_type=return_type
                )

                result = self.backend.generate(program)

                self.assertIn(expected, result)

    def test_rejects_unsupported_binary_and_unary_operators(self):
        cases = [
            IRInstruction("BINARY_?", ["1", "2"], "t1"),
            IRInstruction("UNARY_?", ["1"], "t1")
        ]

        for instruction in cases:
            with self.subTest(opcode=instruction.opcode):
                program = self.make_program([
                    instruction,
                    IRInstruction("RETURN", ["0"])
                ])

                with self.assertRaises(ValueError):
                    self.backend.generate(program)


if __name__ == "__main__":
    unittest.main()
