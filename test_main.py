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

class CourseAverageTests(unittest.TestCase):
    def test_empty_course_average_is_zero(self):
        self.assertEqual(Course("Biochem", 2).get_average_grade(), 0)

    def test_average_for_one_and_two_students(self):
        course = Course("Biochem", 2)
        course.add_student(Student("Craig", 16, 90))
        self.assertEqual(course.get_average_grade(), 90)
        course.add_student(Student("Hancho", 15, 99))
        self.assertAlmostEqual(course.get_average_grade(), 94.5)

    def test_average_uses_updated_grades(self):
        student = Student("Craig", 16, 50)
        course = Course("Biochem", 1)
        course.add_student(student)
        student.set_grade(80)
        self.assertEqual(course.get_average_grade(), 80)

class CourseEnrollmentTests(unittest.TestCase):
    def test_students_can_join_until_the_course_is_full(self):
        course = Course("Biochem", 2)
        craig = Student("Craig", 16, 90)
        hancho = Student("Hancho", 15, 98)
        annete = Student("Annete", 17, 89)
        self.assertTrue(course.add_student(craig))
        self.assertTrue(course.add_student(hancho))
        self.assertFalse(course.add_student(annete))
        self.assertEqual(course.students, [craig, hancho])

    def test_courses_have_separate_student_lists(self):
        biochem = Course("Biochem", 2)
        maths = Course("Maths", 2)
        biochem.add_student(Student("Craig", 16, 90))
        self.assertEqual(maths.students, [])

class DuplicateEnrollmentTests(unittest.TestCase):
    def test_same_student_cannot_join_twice(self):
        course = Course("Biochem", 3)
        student = Student("Craig", 16, 90)
        self.assertTrue(course.add_student(student))
        self.assertFalse(course.add_student(student))
        self.assertEqual(course.students, [student])

    def test_different_objects_can_have_the_same_name(self):
        course = Course("Biochem", 2)
        first = Student("Craig", 16, 90)
        second = Student("Craig", 17, 80)
        self.assertTrue(course.add_student(first))
        self.assertTrue(course.add_student(second))
        self.assertEqual(len(course.students), 2)

class StudentRemovalTests(unittest.TestCase):
    def test_removing_a_student_frees_a_place(self):
        course = Course("Biochem", 1)
        craig = Student("Craig", 16, 90)
        hancho = Student("Hancho", 15, 98)
        course.add_student(craig)
        self.assertFalse(course.add_student(hancho))
        self.assertTrue(course.remove_student(craig))
        self.assertTrue(course.add_student(hancho))
        self.assertEqual(course.students, [hancho])

    def test_removing_an_absent_student_returns_false(self):
        course = Course("Biochem", 1)
        student = Student("Craig", 16, 90)
        self.assertFalse(course.remove_student(student))
        self.assertEqual(course.students, [])

    def test_removing_last_student_resets_average(self):
        course = Course("Biochem", 1)
        student = Student("Craig", 16, 90)
        course.add_student(student)
        course.remove_student(student)
        self.assertEqual(course.get_average_grade(), 0)

class HighestGradeTests(unittest.TestCase):
    def test_empty_course_has_no_highest_grade(self):
        self.assertIsNone(Course("Biochem", 2).get_highest_grade())

    def test_highest_grade_includes_ties_and_updates(self):
        course = Course("Biochem", 3)
        craig = Student("Craig", 16, 90)
        hancho = Student("Hancho", 15, 98)
        annete = Student("Annete", 17, 98)
        for student in (craig, hancho, annete):
            course.add_student(student)
        self.assertEqual(course.get_highest_grade(), 98)
        craig.set_grade(100)
        self.assertEqual(course.get_highest_grade(), 100)

    def test_zero_is_a_valid_highest_grade(self):
        course = Course("Biochem", 1)
        course.add_student(Student("Craig", 16, 0))
        self.assertEqual(course.get_highest_grade(), 0)

class AnimalTests(unittest.TestCase):
    def test_animal_stores_name_and_age(self):
        animal = Animal("dogma", 8)
        self.assertEqual(animal.name, "dogma")
        self.assertEqual(animal.age, 8)

    def test_animal_description_is_printed(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Animal("dogma", 8).what_i_do()
        self.assertEqual(output.getvalue(), "I am dogma, and I am 8 years old\n")

    def test_animal_default_speech_is_printed(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Animal("dogma", 8).speech()
        self.assertEqual(
            output.getvalue(),
            "I am too tired to speak, can you google me??  please!!\n",
        )

class MonkeyInheritanceTests(unittest.TestCase):
    def test_monkey_inherits_the_animal_constructor(self):
        monkey = Monkey("Kabanzy", 13)
        self.assertIsInstance(monkey, Animal)
        self.assertEqual(monkey.name, "Kabanzy")
        self.assertEqual(monkey.age, 13)

    def test_monkey_inherits_the_description_method(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Monkey("Kabanzy", 13).what_i_do()
        self.assertEqual(output.getvalue(), "I am Kabanzy, and I am 13 years old\n")

    def test_monkey_overrides_speech(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Monkey("Kabanzy", 13).speech()
        self.assertEqual(output.getvalue(), "Chappy chappy chapping !!\n")

class PigInheritanceTests(unittest.TestCase):
    def test_super_initializes_parent_attributes(self):
        pig = Pig("fattyme", 6, "red-hot")
        self.assertIsInstance(pig, Animal)
        self.assertEqual(pig.name, "fattyme")
        self.assertEqual(pig.age, 6)
        self.assertEqual(pig.color, "red-hot")

    def test_pig_description_includes_its_color(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Pig("fattyme", 6, "red-hot").what_i_do()
        self.assertEqual(
            output.getvalue(),
            "I am fattyme, and Im 6 years old, my color is red-hot\n",
        )

    def test_pig_overrides_speech(self):
        output = io.StringIO()
        with redirect_stdout(output):
            Pig("fattyme", 6, "red-hot").speech()
        self.assertEqual(output.getvalue(), "ngroooollll !!\n")

    def test_same_method_call_uses_each_animals_implementation(self):
        animals = [Animal("dogma", 8), Monkey("Kabanzy", 13), Pig("fattyme", 6, "red-hot")]
        output = io.StringIO()
        with redirect_stdout(output):
            for animal in animals:
                animal.speech()
        self.assertEqual(output.getvalue().splitlines(), [
            "I am too tired to speak, can you google me??  please!!",
            "Chappy chappy chapping !!",
            "ngroooollll !!",
        ])


class LearningTipsTests(unittest.TestCase):
    """Practice small Python ideas using the same fresh examples in each test."""

    def setUp(self):
        self.students = [
            Student("Craig", 16, 90),
            Student("Hancho", 15, 60),
            Student("Annete", 17, 45),
        ]
        self.course = Course("Python", 3)
        for student in self.students:
            self.course.add_student(student)

    def test_set_up_provides_a_fresh_course(self):
        self.assertEqual(self.course.name, "Python")
        self.assertEqual(self.course.students, self.students)
        self.assertEqual([student.get_grade() for student in self.students], [90, 60, 45])

    def test_list_copy_has_its_own_roster_but_shares_students(self):
        alias = self.course.students
        copied = self.course.students.copy()
        self.assertIs(alias, self.course.students)
        self.assertIsNot(copied, self.course.students)
        copied.pop()
        self.assertEqual(len(copied), 2)
        self.assertEqual(len(self.course.students), 3)
        copied[0].set_grade(80)
        self.assertEqual(self.course.students[0].get_grade(), 80)

    def test_negative_index_reads_the_last_enrolled_student(self):
        last_student = self.course.students[-1]
        self.assertIs(last_student, self.students[2])
        self.assertEqual(last_student.name, "Annete")
        self.assertEqual(self.course.students[-2].name, "Hancho")

if __name__ == "__main__":
    unittest.main()
