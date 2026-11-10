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

    def test_slice_selects_the_first_two_students(self):
        first_two = self.course.students[:2]
        self.assertEqual([student.name for student in first_two], ["Craig", "Hancho"])
        first_two.clear()
        self.assertEqual(len(self.course.students), 3)
        self.assertEqual(self.course.students[10:], [])

    def test_list_comprehension_collects_student_names(self):
        names = [student.name for student in self.course.students]
        self.assertEqual(names, ["Craig", "Hancho", "Annete"])
        self.assertEqual(len(names), len(self.course.students))

    def test_filtered_comprehension_finds_passing_students(self):
        passing_names = [
            student.name for student in self.course.students if student.has_passed()
        ]
        self.assertEqual(passing_names, ["Craig", "Hancho"])
        self.assertEqual(len(self.course.students), 3)

    def test_dictionary_comprehension_builds_a_gradebook(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        self.assertEqual(gradebook, {"Craig": 90, "Hancho": 60, "Annete": 45})
        self.assertEqual(gradebook["Hancho"], 60)

    def test_dictionary_get_supplies_a_missing_value(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        self.assertEqual(gradebook.get("Craig", "Not enrolled"), 90)
        self.assertEqual(gradebook.get("Maya", "Not enrolled"), "Not enrolled")
        self.assertNotIn("Maya", gradebook)

    def test_set_comprehension_removes_duplicate_grades(self):
        self.students[2].set_grade(60)
        unique_grades = {student.get_grade() for student in self.students}
        self.assertEqual(unique_grades, {90, 60})
        self.assertIn(60, unique_grades)
        self.assertEqual(len(unique_grades), 2)

    def test_tuple_unpacking_names_student_details(self):
        student = self.students[0]
        details = (student.name, student.age, student.get_grade())
        name, age, grade = details
        self.assertEqual(name, "Craig")
        self.assertEqual(age, 16)
        self.assertEqual(grade, 90)

    def test_enumerate_numbers_the_roster_from_one(self):
        numbered_names = []
        for number, student in enumerate(self.course.students, start=1):
            numbered_names.append((number, student.name))
        self.assertEqual(numbered_names, [(1, "Craig"), (2, "Hancho"), (3, "Annete")])

    def test_zip_pairs_students_with_grade_updates(self):
        new_grades = [95, 70, 65]
        for student, grade in zip(self.students, new_grades):
            student.set_grade(grade)
        self.assertEqual([student.get_grade() for student in self.students], new_grades)
        self.assertAlmostEqual(self.course.get_average_grade(), 230 / 3)

    def test_sorted_uses_a_key_and_preserves_enrollment_order(self):
        ranked = sorted(self.course.students, key=lambda student: student.get_grade())
        self.assertEqual([student.name for student in ranked], ["Annete", "Hancho", "Craig"])
        self.assertEqual(
            [student.name for student in self.course.students], ["Craig", "Hancho", "Annete"]
        )

    def test_sum_totals_a_stream_of_grades(self):
        total = sum(student.get_grade() for student in self.students)
        self.assertEqual(total, 195)
        self.assertAlmostEqual(total / len(self.students), self.course.get_average_grade())
        self.assertEqual(sum([]), 0)

    def test_any_detects_at_least_one_failing_grade(self):
        needs_help = any(not student.has_passed() for student in self.students)
        self.assertTrue(needs_help)
        self.students[2].set_grade(60)
        self.assertFalse(any(not student.has_passed() for student in self.students))
        self.assertFalse(any([]))

    def test_all_checks_every_passing_result(self):
        self.assertFalse(all(student.has_passed() for student in self.students))
        self.students[2].set_grade(60)
        self.assertTrue(all(student.has_passed() for student in self.students))
        self.assertTrue(all([]))

    def test_empty_lists_are_false_and_populated_lists_are_true(self):
        empty_course = Course("Maths", 2)
        self.assertEqual(len(empty_course.students), 0)
        self.assertFalse(bool(empty_course.students))
        empty_course.add_student(self.students[0])
        self.assertEqual(len(empty_course.students), 1)
        self.assertTrue(bool(empty_course.students))

    def test_next_finds_a_student_or_returns_a_default(self):
        found = next((student for student in self.students if student.name == "Hancho"), None)
        missing = next((student for student in self.students if student.name == "Maya"), None)
        self.assertIs(found, self.students[1])
        self.assertIsNone(missing)

    def test_f_string_formats_the_average_to_one_decimal_place(self):
        message = f"{self.course.name}: average {self.course.get_average_grade():.1f}"
        self.assertEqual(message, "Python: average 65.0")
        self.assertEqual(f"{2 / 3:.2f}", "0.67")
        self.assertEqual(self.course.get_average_grade(), 65)

    def test_course_lifecycle_combines_the_small_lessons(self):
        self.assertEqual(self.course.get_average_grade(), 65)
        self.students[2].set_grade(75)
        self.assertTrue(all(student.has_passed() for student in self.course.students))
        self.assertEqual(self.course.get_average_grade(), 75)
        self.assertTrue(self.course.remove_student(self.students[0]))
        self.assertEqual(self.course.get_highest_grade(), 75)
        maya = Student("Maya", 18, 100)
        self.assertTrue(self.course.add_student(maya))
        self.assertEqual(self.course.get_highest_grade(), 100)
        self.assertAlmostEqual(self.course.get_average_grade(), 235 / 3)
        self.assertEqual([student.name for student in self.course.students], ["Hancho", "Annete", "Maya"])

    def test_uppercase_changes_the_result_not_the_name(self):
        name = self.students[0].name
        self.assertEqual(name.upper(), "CRAIG")
        self.assertEqual(name, "Craig")

    def test_lowercase_changes_capital_letters(self):
        course_name = "PYTHON CLASS"
        self.assertEqual(course_name.lower(), "python class")

    def test_strip_removes_only_outer_spaces(self):
        label = "  Craig  "
        self.assertEqual(label.strip(), "Craig")
        self.assertEqual(label, "  Craig  ")

    def test_startswith_and_endswith_check_text_edges(self):
        name = self.students[0].name
        self.assertTrue(name.startswith("Cr"))
        self.assertTrue(name.endswith("ig"))
        self.assertFalse(name.startswith("Ha"))

    def test_replace_returns_a_string_with_new_text(self):
        label = "Grade: 90"
        self.assertEqual(label.replace("90", "95"), "Grade: 95")
        self.assertEqual(label, "Grade: 90")

    def test_split_turns_text_into_a_list(self):
        names = "Craig,Hancho,Annete".split(",")
        self.assertEqual(names, ["Craig", "Hancho", "Annete"])

    def test_join_connects_list_items_into_text(self):
        names = [student.name for student in self.students]
        self.assertEqual(" / ".join(names), "Craig / Hancho / Annete")

    def test_count_returns_the_number_of_matches(self):
        self.assertEqual("Annete".count("e"), 2)
        self.assertEqual("Annete".count("x"), 0)

    def test_in_checks_for_a_substring(self):
        message = "Craig passed the Python class"
        self.assertTrue("passed" in message)
        self.assertFalse("failed" in message)

    def test_string_index_reads_one_character(self):
        name = self.students[0].name
        self.assertEqual(name[0], "C")
        self.assertEqual(name[-1], "g")

    def test_plus_combines_string_values(self):
        message = self.students[0].name + " passed"
        self.assertEqual(message, "Craig passed")

    def test_int_converts_digit_text_to_an_integer(self):
        grade = int("90")
        self.assertEqual(grade, 90)
        self.assertIsInstance(grade, int)

    def test_float_converts_decimal_text(self):
        average = float("94.5")
        self.assertEqual(average, 94.5)
        self.assertIsInstance(average, float)

    def test_invalid_integer_text_raises_value_error(self):
        with self.assertRaises(ValueError):
            int("ninety")

    def test_round_returns_the_requested_decimal_places(self):
        average = 65.257
        self.assertEqual(round(average, 1), 65.3)
        self.assertEqual(average, 65.257)

    def test_divmod_returns_quotient_and_remainder(self):
        quotient, remainder = divmod(95, 10)
        self.assertEqual(quotient, 9)
        self.assertEqual(remainder, 5)

    def test_remainder_operator_finds_even_numbers(self):
        even_names = [student.name for student in self.students if student.get_grade() % 2 == 0]
        self.assertEqual(even_names, ["Craig", "Hancho"])

    def test_min_returns_the_smallest_grade(self):
        lowest = min(student.get_grade() for student in self.students)
        self.assertEqual(lowest, 45)
        self.assertEqual(self.students[2].name, "Annete")

    def test_max_returns_the_largest_grade(self):
        highest = max(student.get_grade() for student in self.students)
        self.assertEqual(highest, 90)
        self.assertEqual(self.students[0].name, "Craig")

    def test_sorted_reverse_orders_grades_descending(self):
        ranked = sorted(self.students, key=lambda student: student.get_grade(), reverse=True)
        self.assertEqual([student.name for student in ranked], ["Craig", "Hancho", "Annete"])
        self.assertEqual([student.name for student in self.course.students], ["Craig", "Hancho", "Annete"])

    def test_append_adds_an_item_to_the_end(self):
        names = [student.name for student in self.students]
        names.append("Maya")
        self.assertEqual(names, ["Craig", "Hancho", "Annete", "Maya"])
        self.assertEqual(len(self.course.students), 3)

    def test_remove_deletes_the_matching_list_item(self):
        names = [student.name for student in self.students]
        names.remove("Hancho")
        self.assertEqual(names, ["Craig", "Annete"])
        self.assertEqual(len(self.course.students), 3)

    def test_in_finds_an_enrolled_student(self):
        self.assertIn(self.students[1], self.course.students)
        self.assertIn(self.students[1].name, [student.name for student in self.course.students])

    def test_not_in_finds_a_student_who_is_absent(self):
        maya = Student("Maya", 18, 88)
        self.assertNotIn(maya, self.course.students)
        self.assertTrue(self.course.remove_student(self.students[0]))
        self.assertTrue(self.course.add_student(maya))
        self.assertIn(maya, self.course.students)

    def test_tuple_indexes_select_values(self):
        details = ("Craig", 16, 90)
        self.assertEqual(details[0], "Craig")
        self.assertEqual(details[-1], 90)

    def test_tuple_assignment_raises_type_error(self):
        details = ("Craig", 16, 90)
        with self.assertRaises(TypeError):
            details[0] = "Anne"
        self.assertEqual(details[0], "Craig")

    def test_keys_lists_each_gradebook_name(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        self.assertEqual(set(gradebook.keys()), {"Craig", "Hancho", "Annete"})

    def test_values_lists_each_grade(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        self.assertEqual(list(gradebook.values()), [90, 60, 45])

    def test_items_returns_name_and_grade_pairs(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        pairs = list(gradebook.items())
        self.assertEqual(pairs[0], ("Craig", 90))
        self.assertEqual(len(pairs), 3)

    def test_dictionary_assignment_updates_a_grade(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        gradebook["Craig"] = 95
        self.assertEqual(gradebook["Craig"], 95)
        self.assertEqual(self.students[0].get_grade(), 90)

    def test_dictionary_pop_returns_and_removes_a_value(self):
        gradebook = {student.name: student.get_grade() for student in self.students}
        removed_grade = gradebook.pop("Annete")
        self.assertEqual(removed_grade, 45)
        self.assertNotIn("Annete", gradebook)
        self.assertEqual(self.students[2].get_grade(), 45)

    def test_intersection_finds_grades_in_both_sets(self):
        class_grades = {90, 60, 45}
        honor_roll_grades = {100, 90}
        self.assertEqual(class_grades.intersection(honor_roll_grades), {90})

    def test_union_combines_unique_grades(self):
        class_grades = {90, 60, 45}
        new_grades = {100, 90}
        self.assertEqual(class_grades.union(new_grades), {100, 90, 60, 45})
        self.assertEqual(class_grades, {90, 60, 45})

    def test_floor_division_returns_a_whole_quotient(self):
        self.assertEqual(95 // 10, 9)
        self.assertEqual(95 / 10, 9.5)

    def test_abs_returns_a_non_negative_distance(self):
        self.assertEqual(abs(-45), 45)
        self.assertEqual(abs(45), 45)
        self.assertEqual(abs(0), 0)

    def test_insert_places_an_item_at_an_index(self):
        names = [student.name for student in self.students]
        names.insert(1, "Maya")
        self.assertEqual(names, ["Craig", "Maya", "Hancho", "Annete"])

    def test_extend_adds_each_item_from_another_list(self):
        names = [student.name for student in self.students]
        names.extend(["Maya", "Lee"])
        self.assertEqual(names, ["Craig", "Hancho", "Annete", "Maya", "Lee"])

    def test_reverse_changes_the_list_order(self):
        names = [student.name for student in self.students]
        names.reverse()
        self.assertEqual(names, ["Annete", "Hancho", "Craig"])
        self.assertEqual([student.name for student in self.course.students], ["Craig", "Hancho", "Annete"])

    def test_index_returns_the_first_matching_position(self):
        names = [student.name for student in self.students]
        self.assertEqual(names.index("Hancho"), 1)

    def test_slice_step_selects_every_other_name(self):
        names = [student.name for student in self.students]
        self.assertEqual(names[::2], ["Craig", "Annete"])

    def test_range_counts_up_to_but_not_including_the_stop(self):
        numbers = list(range(1, 5))
        self.assertEqual(numbers, [1, 2, 3, 4])

    def test_reversed_returns_items_in_reverse_order(self):
        names = [student.name for student in self.students]
        backwards = list(reversed(names))
        self.assertEqual(backwards, ["Annete", "Hancho", "Craig"])
        self.assertEqual(names[0], "Craig")

    def test_setdefault_adds_only_a_missing_key(self):
        gradebook = {"Craig": 90}
        self.assertEqual(gradebook.setdefault("Maya", 0), 0)
        self.assertEqual(gradebook.setdefault("Craig", 0), 90)
        self.assertEqual(gradebook, {"Craig": 90, "Maya": 0})

    def test_update_adds_and_replaces_dictionary_entries(self):
        gradebook = {"Craig": 90}
        gradebook.update({"Craig": 95, "Maya": 80})
        self.assertEqual(gradebook, {"Craig": 95, "Maya": 80})

    def test_del_removes_a_dictionary_entry(self):
        gradebook = {"Craig": 90, "Maya": 80}
        del gradebook["Maya"]
        self.assertEqual(gradebook, {"Craig": 90})
        self.assertNotIn("Maya", gradebook)

    def test_filtered_dictionary_keeps_passing_students(self):
        passing = {student.name: student.get_grade() for student in self.students if student.has_passed()}
        self.assertEqual(passing, {"Craig": 90, "Hancho": 60})

    def test_issubset_checks_that_every_value_is_present(self):
        course_grades = {student.get_grade() for student in self.students}
        passing_grades = {60, 90}
        self.assertTrue(passing_grades.issubset(course_grades))
        self.assertFalse({100}.issubset(course_grades))

    def test_difference_returns_values_missing_from_the_other_set(self):
        course_grades = {90, 60, 45}
        honor_roll = {90, 100}
        self.assertEqual(course_grades.difference(honor_roll), {60, 45})

    def test_conditional_expression_selects_a_label(self):
        student = self.students[0]
        label = "pass" if student.has_passed() else "try again"
        self.assertEqual(label, "pass")
        student = self.students[2]
        label = "pass" if student.has_passed() else "try again"
        self.assertEqual(label, "try again")

    def test_for_loop_accumulates_the_student_grades(self):
        total = 0
        for student in self.students:
            total += student.get_grade()
        self.assertEqual(total, 195)

    def test_break_stops_after_the_first_passing_student(self):
        first_passing = None
        for student in self.students:
            if student.has_passed():
                first_passing = student.name
                break
        self.assertEqual(first_passing, "Craig")

    def test_while_loop_counts_three_steps(self):
        steps = 0
        while steps < 3:
            steps += 1
        self.assertEqual(steps, 3)

    def test_local_function_reuses_a_passing_check(self):
        def describe(student):
            return f"{student.name}: {student.get_grade()}"
        self.assertEqual(describe(self.students[0]), "Craig: 90")
        self.assertEqual(describe(self.students[1]), "Hancho: 60")

    def test_try_except_uses_a_fallback_for_bad_text(self):
        try:
            grade = int("ninety")
        except ValueError:
            grade = 0
        self.assertEqual(grade, 0)

    def test_none_check_distinguishes_a_missing_match(self):
        missing = next((student for student in self.students if student.name == "Maya"), None)
        self.assertIsNone(missing)
        found = next((student for student in self.students if student.name == "Craig"), None)
        self.assertIsNotNone(found)

    def test_capitalize_changes_the_first_letter(self):
        self.assertEqual("craig".capitalize(), "Craig")

    def test_title_capitalizes_each_word(self):
        self.assertEqual("python class".title(), "Python Class")

    def test_swapcase_flips_letter_case(self):
        self.assertEqual("Craig Passed".swapcase(), "cRAIG pASSED")

    def test_find_returns_the_position_or_negative_one(self):
        message = "Craig passed"
        self.assertEqual(message.find("passed"), 6)
        self.assertEqual(message.find("failed"), -1)

    def test_partition_returns_before_separator_and_after(self):
        before, separator, after = "Grade: 90".partition(": ")
        self.assertEqual((before, separator, after), ("Grade", ": ", "90"))

    def test_removeprefix_removes_only_the_starting_text(self):
        label = "Grade: 90"
        self.assertEqual(label.removeprefix("Grade: "), "90")
        self.assertEqual(label.removeprefix("Score: "), label)

    def test_isdecimal_checks_digit_text(self):
        self.assertTrue("2026".isdecimal())
        self.assertFalse("20.26".isdecimal())
        self.assertFalse("twenty".isdecimal())

    def test_f_string_can_pad_a_number(self):
        self.assertEqual(f"{7:03}", "007")
        self.assertEqual(f"{90:03}", "090")

    def test_string_slice_returns_a_section(self):
        name = "Craig"
        self.assertEqual(name[1:4], "rai")
        self.assertEqual(name, "Craig")

    def test_list_count_counts_matching_values(self):
        names = ["Craig", "Hancho", "Craig"]
        self.assertEqual(names.count("Craig"), 2)
        self.assertEqual(names.count("Maya"), 0)

    def test_pop_returns_and_removes_the_last_list_item(self):
        names = [student.name for student in self.students]
        last_name = names.pop()
        self.assertEqual(last_name, "Annete")
        self.assertEqual(names, ["Craig", "Hancho"])

    def test_clear_empties_a_list_in_place(self):
        names = [student.name for student in self.students]
        names.clear()
        self.assertEqual(names, [])
        self.assertEqual(len(self.course.students), 3)

    def test_sort_changes_a_list_and_returns_none(self):
        names = ["Annete", "Craig", "Hancho"]
        result = names.sort()
        self.assertEqual(names, ["Annete", "Craig", "Hancho"])
        self.assertIsNone(result)

    def test_list_index_assignment_changes_one_item(self):
        names = [student.name for student in self.students]
        names[1] = "Maya"
        self.assertEqual(names, ["Craig", "Maya", "Annete"])

    def test_starred_unpacking_collects_remaining_items(self):
        grades = [90, 60, 45]
        first, *remaining = grades
        self.assertEqual(first, 90)
        self.assertEqual(remaining, [60, 45])

    def test_tuple_count_finds_repeated_values(self):
        scores = (90, 75, 90, 60)
        self.assertEqual(scores.count(90), 2)
        self.assertEqual(scores.count(100), 0)

    def test_add_places_a_new_value_in_a_set(self):
        grades = {90, 60}
        grades.add(45)
        self.assertEqual(grades, {90, 60, 45})

    def test_discard_removes_a_value_if_present(self):
        grades = {90, 60}
        grades.discard(60)
        grades.discard(45)
        self.assertEqual(grades, {90})

    def test_issuperset_checks_all_requested_values(self):
        grades = {90, 60, 45}
        self.assertTrue(grades.issuperset({60, 45}))
        self.assertFalse(grades.issuperset({60, 100}))

    def test_update_adds_all_values_from_another_collection(self):
        grades = {90}
        grades.update([60, 45, 90])
        self.assertEqual(grades, {90, 60, 45})

    def test_fromkeys_builds_a_dictionary(self):
        gradebook = dict.fromkeys(["Craig", "Hancho"], 0)
        self.assertEqual(gradebook, {"Craig": 0, "Hancho": 0})

    def test_dictionary_copy_can_change_separately(self):
        original = {"Craig": 90}
        copied = original.copy()
        copied["Maya"] = 80
        self.assertEqual(original, {"Craig": 90})
        self.assertEqual(copied, {"Craig": 90, "Maya": 80})

    def test_popitem_returns_the_last_added_pair(self):
        gradebook = {"Craig": 90, "Maya": 80}
        name, grade = gradebook.popitem()
        self.assertEqual((name, grade), ("Maya", 80))
        self.assertEqual(gradebook, {"Craig": 90})

    def test_in_checks_dictionary_keys(self):
        gradebook = {"Craig": 90, "Maya": 80}
        self.assertIn("Craig", gradebook)
        self.assertNotIn("Annete", gradebook)
        self.assertIn(90, gradebook.values())

    def test_double_star_calculates_a_power(self):
        self.assertEqual(2 ** 3, 8)
        self.assertEqual(10 ** 2, 100)

    def test_chained_comparison_checks_both_limits(self):
        grade = 90
        self.assertTrue(0 <= grade <= 100)
        self.assertFalse(0 <= 101 <= 100)

    def test_bool_converts_values_to_truth_values(self):
        self.assertFalse(bool(0))
        self.assertTrue(bool(1))
        self.assertTrue(bool("hello"))
        self.assertFalse(bool(""))

    def test_plus_equals_adds_to_a_value(self):
        grade = 90
        grade += 5
        self.assertEqual(grade, 95)
        grade -= 10
        self.assertEqual(grade, 85)

    def test_subtraction_finds_remaining_capacity(self):
        remaining = self.course.max_students - len(self.course.students)
        self.assertEqual(remaining, 0)
        small_course = Course("Maths", 5)
        self.assertEqual(small_course.max_students - len(small_course.students), 5)

    def test_default_argument_is_used_when_omitted(self):
        def greeting(name, word="Hello"):
            return f"{word}, {name}!"
        self.assertEqual(greeting("Craig"), "Hello, Craig!")
        self.assertEqual(greeting("Maya", "Welcome"), "Welcome, Maya!")

    def test_star_args_collects_extra_values(self):
        def total(*numbers):
            return sum(numbers)
        self.assertEqual(total(90, 60, 45), 195)
        self.assertEqual(total(10), 10)

    def test_double_star_args_collects_named_values(self):
        def student_label(**details):
            return f"{details['name']}: {details['grade']}"
        self.assertEqual(student_label(name="Craig", grade=90), "Craig: 90")

    def test_map_converts_each_grade_to_text(self):
        grades = [student.get_grade() for student in self.students]
        labels = list(map(str, grades))
        self.assertEqual(labels, ["90", "60", "45"])

    def test_filter_keeps_grades_that_pass_a_condition(self):
        grades = [student.get_grade() for student in self.students]
        passing = list(filter(lambda grade: grade >= 60, grades))
        self.assertEqual(passing, [90, 60])

    def test_isinstance_checks_a_values_type(self):
        self.assertTrue(isinstance(90, int))
        self.assertTrue(isinstance(94.5, float))
        self.assertFalse(isinstance("90", int))

    def test_and_requires_both_conditions_to_be_true(self):
        grade = self.students[0].get_grade()
        self.assertTrue(grade >= 60 and grade <= 100)
        self.assertFalse(grade < 60 and grade <= 100)

    def test_or_can_provide_a_default_value(self):
        grade = None
        shown_grade = grade or 0
        self.assertEqual(shown_grade, 0)
        grade = 90
        self.assertEqual(grade or 0, 90)

    def test_not_flips_a_boolean_result(self):
        self.assertFalse(not self.students[0].has_passed())
        self.assertTrue(not self.students[2].has_passed())

    def test_equal_values_can_be_different_objects(self):
        first = [90, 60]
        second = [90, 60]
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIs(first, first)

    def test_str_converts_a_grade_to_text(self):
        label = str(self.students[0].get_grade())
        self.assertEqual(label, "90")
        self.assertIsInstance(label, str)

    def test_int_truncates_a_decimal_towards_zero(self):
        self.assertEqual(int(94.9), 94)
        self.assertEqual(int(-2.9), -2)

    def test_pow_calculates_an_exponent(self):
        self.assertEqual(pow(2, 3), 8)
        self.assertEqual(pow(5, 2), 25)

    def test_multiplication_happens_before_addition(self):
        self.assertEqual(2 + 3 * 4, 14)

    def test_parentheses_make_addition_happen_first(self):
        self.assertEqual((2 + 3) * 4, 20)

    def test_unary_minus_changes_the_sign(self):
        grade_change = -10
        self.assertEqual(90 + grade_change, 80)
        self.assertEqual(-(-10), 10)

    def test_multiple_assignment_swaps_two_values(self):
        first, second = "Craig", "Hancho"
        first, second = second, first
        self.assertEqual(first, "Hancho")
        self.assertEqual(second, "Craig")

    def test_two_indexes_read_a_nested_value(self):
        grades = [[90, 80], [70, 60]]
        self.assertEqual(grades[0][1], 80)
        self.assertEqual(grades[1][0], 70)

    def test_for_loop_unpacks_each_pair(self):
        records = [("Craig", 90), ("Hancho", 60)]
        labels = []
        for name, grade in records:
            labels.append(f"{name}: {grade}")
        self.assertEqual(labels, ["Craig: 90", "Hancho: 60"])

    def test_dictionary_items_can_be_unpacked_in_a_loop(self):
        gradebook = {"Craig": 90, "Hancho": 60}
        labels = []
        for name, grade in gradebook.items():
            labels.append(f"{name}: {grade}")
        self.assertEqual(labels, ["Craig: 90", "Hancho: 60"])

    def test_keyword_arguments_name_their_values(self):
        def greeting(name, word):
            return f"{word}, {name}!"
        self.assertEqual(greeting(name="Craig", word="Hello"), "Hello, Craig!")
        self.assertEqual(greeting(word="Welcome", name="Maya"), "Welcome, Maya!")

    def test_format_specifier_aligns_text(self):
        self.assertEqual(f"{'Craig':>8}", "   Craig")
        self.assertEqual(f"{'Craig':<8}", "Craig   ")

if __name__ == "__main__":
    unittest.main()
