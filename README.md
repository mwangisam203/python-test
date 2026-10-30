# Python class practice

This project teaches Python classes with `Student`, `Course`, `Animal`, `Monkey`,
and `Pig`. Each numbered lesson has its own Git commit and tests in `test_main.py`.
Read the lessons below alongside the code; the tests show concrete inputs and
expected results.

Run the examples from this directory:

```bash
python3 main.py
```

Run all tests (Python standard library only; no packages to install):

```bash
python3 -m unittest -v
```

Run just one lesson's tests, for example:

```bash
python3 -m unittest -v test_main.ImportTests
```

## Lessons

1. **Run examples only when the file is executed.** `if __name__ == "__main__"` calls `main()` when you run `python3 main.py`. Importing the classes for tests prints nothing. `ImportTests` checks this in a fresh Python process.

2. **Test instance attributes.** `__init__` stores values on `self`. `StudentAttributeTests` checks Craig's name, age, and grade, then changes another student's name to show that each object keeps its own attributes.

3. **Test a method return value.** `get_grade()` returns the stored number. `StudentGradeTests` tries 0, 89.5, and 100; `subTest` labels each input so a failure identifies the grade that caused it.

4. **Keep grades between zero and one hundred.** The constructor raises `ValueError` for numeric grades outside 0–100. `GradeValidationTests` checks -1 and 101 are rejected while 0 and 100 are accepted.

5. **Use a default argument for a passing mark.** `has_passed()` uses 60 unless a caller supplies another mark. `PassingGradeTests` checks 59 fails and 60 passes, then checks a grade of 75 against custom marks of 70 and 80.

6. **Validate grade updates in one method.** `set_grade()` checks the range before assigning the new value, and `__init__` reuses it. `GradeUpdateTests` updates 50 to 85 and verifies an invalid update leaves the old grade unchanged. Use this method for updates; assigning `.grade` directly bypasses the check.

7. **Require a positive course capacity.** `Course("Biochem", 2)` creates two available places and an empty student list. `CourseCapacityTests` rejects zero, negative numbers, decimals, strings, booleans, and `None`. `type(max_students) is int` requires an actual integer, so `True` is rejected too.

8. **Handle empty and populated course averages.** `get_average_grade()` returns 0 for an empty course to avoid dividing by zero. `CourseAverageTests` checks one grade of 90, the average of 90 and 99 (94.5), and a grade update. `assertAlmostEqual` is useful when comparing decimal calculations.

9. **Test enrollment at the capacity limit.** `add_student()` returns `True` when a student joins and `False` when the course is full. `CourseEnrollmentTests` fills two places, rejects the third student, and checks that separate courses have separate student lists.

10. **Prevent duplicate enrollment.** `student in self.students` stops the same student object from taking two places. `DuplicateEnrollmentTests` checks this even when space remains. Two different student objects may share a name and still enroll because no custom equality method is defined.

11. **Remove a student from a list.** `remove_student()` returns `True` after removal or `False` if the student is absent. `StudentRemovalTests` shows that removing a student frees a place and removing the last student makes the course average 0 again.

12. **Find the highest grade with max.** `max(student.get_grade() for student in self.students)` finds the largest current grade. `HighestGradeTests` checks ties, updates, and a grade of 0. An empty course returns `None`, which means no result rather than a score of zero.

13. **Capture printed output in a test.** `AnimalTests` checks the base class attributes and printed messages. `io.StringIO()` stores text in memory; `redirect_stdout(output)` captures `print()` inside its `with` block. The expected strings include the final newline (`\n`).

14. **Test inheritance and method overriding.** `Monkey(Animal)` inherits `__init__` and `what_i_do()` but defines its own `speech()`. `MonkeyInheritanceTests` checks the inherited attributes and description, then verifies the monkey prints its own sound. `assertIsInstance(monkey, Animal)` checks the parent relationship.

15. **Test super and polymorphism.** `Pig.__init__` calls `super().__init__(name, age)` to set the parent attributes, then adds `color`. `PigInheritanceTests` checks those attributes and both overridden methods. Its final test loops through three animal types and calls `speech()` on each: Python chooses the method for the actual object. This behavior is called polymorphism.

## More practice: lessons 16–35

These twenty lessons use `LearningTipsTests` in `test_main.py`. Run them with `python3 -m unittest -v test_main.LearningTipsTests`.

16. **Reuse fresh examples with setUp.** `LearningTipsTests.setUp()` runs before every test in that class. It creates a Python course and three students: Craig (90), Hancho (60), and Annete (45). Every test starts with fresh objects, so changing a grade in one test does not change another test. `test_set_up_provides_a_fresh_course` checks these starting values.

17. **Compare a list alias with a shallow copy.** `alias = course.students` refers to the same list. `.copy()` creates another list: popping from the copy leaves the original with three students. This is a shallow copy, so both lists still refer to the same student objects. Changing the copied list's first student to grade 80 also changes the original student.

18. **Read the last item with a negative index.** List indexes start at zero from the front. Negative indexes count from the end: `students[-1]` is Annete and `students[-2]` is Hancho. An index must exist; indexing an empty list raises `IndexError`.
