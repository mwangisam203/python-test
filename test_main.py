"""Small examples of unittest assertions for the classes in main.py."""

from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import unittest

from main import Animal, Course, Monkey, Pig, Student


class ImportTests(unittest.TestCase):
    def test_import_does_not_run_examples(self):
        result = subprocess.run(
            [sys.executable, "-c", "import main"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

if __name__ == "__main__":
    unittest.main()
