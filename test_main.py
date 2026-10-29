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

class GradeValidationTests(unittest.TestCase):
    def test_out_of_range_grades_raise_value_error(self):
        for grade in (-1, 101):
            with self.subTest(grade=grade):
                with self.assertRaisesRegex(ValueError, "between 0 and 100"):
                    Student("Craig", 16, grade)

    def test_boundary_grades_are_allowed(self):
        self.assertEqual(Student("Craig", 16, 0).get_grade(), 0)
        self.assertEqual(Student("Craig", 16, 100).get_grade(), 100)

class PassingGradeTests(unittest.TestCase):
    def test_default_passing_mark_is_sixty(self):
        self.assertFalse(Student("Craig", 16, 59).has_passed())
        self.assertTrue(Student("Hancho", 15, 60).has_passed())

    def test_passing_mark_can_be_supplied(self):
        student = Student("Annete", 17, 75)
        self.assertTrue(student.has_passed(70))
        self.assertFalse(student.has_passed(80))

class GradeUpdateTests(unittest.TestCase):
    def test_grade_can_be_updated(self):
        student = Student("Craig", 16, 50)
        student.set_grade(85)
        self.assertEqual(student.get_grade(), 85)
        self.assertTrue(student.has_passed())

    def test_invalid_update_keeps_previous_grade(self):
        student = Student("Craig", 16, 90)
        for grade in (-1, 101):
            with self.subTest(grade=grade):
                with self.assertRaises(ValueError):
                    student.set_grade(grade)
                self.assertEqual(student.get_grade(), 90)

class CourseCapacityTests(unittest.TestCase):
    def test_capacity_must_be_a_positive_integer(self):
        for capacity in (0, -1, 2.5, "2", True, None):
            with self.subTest(capacity=capacity):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    Course("Biochem", capacity)

    def test_course_starts_with_an_empty_student_list(self):
        course = Course("Biochem", 2)
        self.assertEqual(course.name, "Biochem")
        self.assertEqual(course.max_students, 2)
        self.assertEqual(course.students, [])

if __name__ == "__main__":
    unittest.main()
