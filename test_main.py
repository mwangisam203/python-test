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

class StudentAttributeTests(unittest.TestCase):
    def test_constructor_stores_name_age_and_grade(self):
        student = Student("Craig", 16, 90)
        self.assertEqual(student.name, "Craig")
        self.assertEqual(student.age, 16)
        self.assertEqual(student.grade, 90)

    def test_students_have_separate_attributes(self):
        craig = Student("Craig", 16, 90)
        annete = Student("Annete", 17, 89)
        annete.name = "Anne"
        self.assertEqual(craig.name, "Craig")
        self.assertEqual(annete.name, "Anne")

class StudentGradeTests(unittest.TestCase):
    def test_get_grade_returns_the_students_grade(self):
        for grade in (0, 89.5, 100):
            with self.subTest(grade=grade):
                student = Student("Craig", 16, grade)
                self.assertEqual(student.get_grade(), grade)

if __name__ == "__main__":
    unittest.main()
