import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_RESULTS = {
    "cli_test.cm": 30,
    "name_collision.cm": 30,
    "scope_test.cm": 10,
    "srs_b1.cm": 0,
    "srs_b2.cm": 0,
    "srs_b3.cm": 0,
    "srs_b4.cm": 0,
}


@unittest.skipUnless(
    shutil.which("gcc") and shutil.which("llc"),
    "GCC and LLVM llc are required",
)
class TestEndToEnd(unittest.TestCase):

    def compile_and_run(self, source_path, directory):
        assembly_path = directory / (source_path.stem + ".s")
        executable_path = directory / source_path.stem

        compilation = subprocess.run(
            [
                sys.executable, "-m", "src.main",
                str(source_path), "-o", str(assembly_path),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(
            compilation.returncode, 0,
            compilation.stdout + compilation.stderr,
        )
        self.assertTrue(assembly_path.exists())

        linking = subprocess.run(
            ["gcc", str(assembly_path), "-o", str(executable_path)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(
            linking.returncode, 0,
            linking.stdout + linking.stderr,
        )

        execution = subprocess.run(
            [str(executable_path)],
            capture_output=True,
            text=True,
            timeout=5,
        )

        return execution.returncode

    def test_all_example_programs(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)

            for filename, expected in EXAMPLE_RESULTS.items():
                with self.subTest(example=filename):
                    source_path = PROJECT_ROOT / "examples" / filename
                    actual = self.compile_and_run(source_path, directory)
                    self.assertEqual(actual, expected)

    def test_logical_operators_short_circuit_at_runtime(self):
        source = """
        int main(void) {
            int x = 0;

            if (0 && (x = 1)) {
                return 10;
            }

            if (x != 0) {
                return 1;
            }

            if (1 || (x = 2)) {
                return x;
            }

            return 2;
        }
        """

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source_path = directory / "short_circuit.cm"
            source_path.write_text(source, encoding="utf-8")

            actual = self.compile_and_run(source_path, directory)
            self.assertEqual(actual, 0)


    def test_backend_failure_preserves_existing_assembly(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            assembly_path = directory / "preserve.s"
            original = "ORIGINAL ASSEMBLY — MUST SURVIVE\\n"
            assembly_path.write_text(original, encoding="utf-8")

            env = os.environ.copy()
            env["PATH"] = str(directory)

            result = subprocess.run(
                [
                    sys.executable, "-m", "src.main",
                    str(PROJECT_ROOT / "examples" / "srs_b3.cm"),
                    "-o", str(assembly_path),
                ],
                cwd=PROJECT_ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Required file or tool not found", result.stderr)
            self.assertEqual(
                assembly_path.read_text(encoding="utf-8"),
                original,
            )
            self.assertEqual(
                list(directory.glob(".*.s.tmp")),
                [],
            )



if __name__ == "__main__":
    unittest.main()
