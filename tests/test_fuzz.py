import unittest
import subprocess
import sys
import tempfile
from pathlib import Path


class TestMalformedInputs(unittest.TestCase):

    def test_100_malformed_inputs_do_not_crash(self):
        malformed_inputs = [
            "",
            "int",
            "int main",
            "int main(",
            "int main(void",
            "int main(void) {",
            "int main(void) }",
            "int main(void) { return; }",
            "int main(void) { int x = ; return 0; }",
            "int main(void) { return 0 }",
        ]

        # Generate 90 malformed programs across 9 different categories.
        for i in range(10):
            malformed_inputs.extend([
                f"int main(void) {{ int value{i} = ; return 0; }}",
                f"int main(void) {{ int value{i} = {i} return 0; }}",
                f"int main(void) {{ return ({i} + 1; }}",
                f"int main(void) {{ return {i} * ; }}",
                f"int main(void) {{ if ({i} > ) return 1; return 0; }}",
                f"int main(void) {{ while ({i} < ) {{ return 1; }} return 0; }}",
                f"int main(void) {{ for (int j{i} = 0; j{i} < ; j{i} = j{i} + 1) {{ }} return 0; }}",
                f"int main(void) {{ return missing{i}; }}",
                f"int main(void) {{ missing_function{i}(); return 0; }}",
            ])

        self.assertEqual(len(malformed_inputs), 100)
        self.assertEqual(len(set(malformed_inputs)), 100)

        accepted_diagnostics = (
            "ERROR ",
            "Compilation error:",
            "Semantic error:",
            "NAME_ERROR:",
            "TYPE_ERROR:",
            "CALL_ERROR:",
            "RETURN_ERROR:",
            "CONTROL_FLOW_ERROR:",
            "SEMANTIC_ERROR:",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            for index, source in enumerate(malformed_inputs):
                with self.subTest(input_index=index, source=source):
                    source_file = Path(temp_dir) / f"input_{index}.cm"
                    source_file.write_text(source, encoding="utf-8")

                    result = subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "src.main",
                            str(source_file),
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )

                    self.assertEqual(
                        result.returncode,
                        1,
                        f"Malformed input {index} returned "
                        f"{result.returncode}.\n"
                        f"stdout: {result.stdout}\n"
                        f"stderr: {result.stderr}",
                    )

                    self.assertTrue(
                        result.stderr.startswith(accepted_diagnostics),
                        f"Malformed input {index} did not produce "
                        f"a recognized compiler diagnostic.\n"
                        f"stderr: {result.stderr}",
                    )

                    self.assertNotIn(
                        "Traceback (most recent call last)",
                        result.stderr,
                    )

                    self.assertNotIn(
                        "Unexpected compilation error:",
                        result.stderr,
                    )


if __name__ == "__main__":
    unittest.main()
