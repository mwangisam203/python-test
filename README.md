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

19. **Select part of a list with a slice.** `students[:2]` selects indexes 0 and 1; the stop index is excluded. The slice creates a new list, so clearing it leaves the course roster unchanged. Unlike indexing, slicing past the end is allowed: `[10:]` returns `[]`.

20. **Build a list of names with a comprehension.** `[student.name for student in course.students]` collects one name per student, in enrollment order. The result is `["Craig", "Hancho", "Annete"]`. A list comprehension is a short way to build a list from a loop.

21. **Filter a comprehension with a condition.** Adding `if student.has_passed()` keeps only students whose grades meet the default passing mark of 60. Craig (90) and Hancho (60) are selected; Annete (45) is left out. Filtering creates a result without removing anyone from the course.

22. **Map names to grades with a dictionary.** `{student.name: student.get_grade() for student in students}` builds a dictionary. `gradebook["Hancho"]` looks up 60 by name. Dictionary keys are unique: this example assumes different names; duplicate names would overwrite an earlier entry.

23. **Use get for an optional dictionary entry.** `gradebook.get("Maya", "Not enrolled")` returns the supplied default because Maya is absent. An existing key still returns its grade: `get("Craig", "Not enrolled")` is 90. Calling `.get()` does not add the missing key.

24. **Collect unique values with a set.** After changing Annete's grade to 60, the grades are 90, 60, and 60. `{student.get_grade() for student in students}` produces the set `{90, 60}`. Sets keep unique values; compare membership or whole sets rather than relying on display order.

25. **Unpack a tuple into named variables.** `details = ("Craig", 16, 90)` groups three values in a tuple. `name, age, grade = details` unpacks them in order. The number of variables must match the values unless a starred variable is used.

26. **Number loop items with enumerate.** `enumerate(course.students, start=1)` supplies a counter and a student on each loop iteration. It produces `(1, "Craig")`, `(2, "Hancho")`, and `(3, "Annete")` here. Without `start=1`, counting begins at zero.

27. **Pair students and new grades with zip.** `zip(students, [95, 70, 65])` pairs each student with a new grade. The loop calls `set_grade()` for each pair, and the course average becomes `230 / 3`. By default, `zip()` stops at the shorter input; these inputs both have three items.

28. **Sort by a grade without changing the roster.** `sorted(students, key=lambda student: student.get_grade())` returns a new list in ascending grade order: Annete (45), Hancho (60), Craig (90). The small `lambda` function supplies the value used for sorting. The course keeps its enrollment order.

29. **Total grades with sum.** `sum(student.get_grade() for student in students)` adds 90 + 60 + 45 to get 195. Dividing by the three students gives the course average of 65. `sum([])` returns 0; dividing by the length of an empty list would still raise `ZeroDivisionError`.

30. **Ask whether any student needs help.** `any(not student.has_passed() for student in students)` is `True` while Annete has 45. Raising her grade to 60 makes it `False`. `any()` answers whether at least one item is true; an empty input gives `False`.

31. **Ask whether all students pass.** `all(student.has_passed() for student in students)` starts as `False` and becomes `True` after Annete reaches 60. `all([])` also returns `True` because no item fails the condition. Check that a course has students separately if that matters.

32. **Check whether a roster is empty.** An empty list has length 0 and is false in a condition. After enrollment, the roster has length 1 and is true. This is why `if not self.students` works as the empty-course check in `get_average_grade()`.

33. **Find the first match with next.** `next((student for student in students if student.name == "Hancho"), None)` returns the first matching student. Looking for Maya returns the default `None`. Supplying a default avoids `StopIteration` when there is no match.

34. **Format a decimal inside an f-string.** `f"{course.name}: average {course.get_average_grade():.1f}"` produces `Python: average 65.0`. The format `.1f` displays one decimal place; `.2f` displays two, so `2 / 3` becomes `"0.67"`. Formatting creates text and does not change the numeric grade.

35. **Combine enrollment updates and removal in one exercise.** Start with an average of 65. Raise Annete from 45 to 75: all three students now pass and the average is 75. Remove Craig (90), then enroll Maya (100). The roster becomes Hancho, Annete, Maya; its highest grade is 100 and its average is `235 / 3`. This final test checks the methods working together.

36. **Make a name uppercase.** `name.upper()` returns `"CRAIG"`. It makes a new string and leaves the original name `"Craig"` unchanged.

37. **Make a course name lowercase.** `lower()` changes uppercase letters to lowercase and leaves spaces in place. The original `course_name` remains `"PYTHON CLASS"`.

38. **Remove spaces at the ends of text.** `strip()` removes whitespace from both ends of a string. It leaves spaces inside the string alone and returns a new string.

39. **Check the beginning and ending of a name.** `startswith()` and `endswith()` check text at the beginning or end. They return `True` or `False` and are case sensitive.

40. **Replace text in a string.** `replace("90", "95")` returns `"Grade: 95"`. The original label remains unchanged, as strings cannot be edited in place.

41. **Split a comma separated list.** Calling `.split(",")` cuts the text at each comma and returns a list of three names.

42. **Join names with a separator.** `" / ".join(names)` places the separator between each item and returns one string. The separator goes before `.join()`.

43. **Count a letter in text.** `.count("e")` returns how many times that exact, case sensitive text appears. When it does not appear, `.count()` returns 0.

44. **Check whether text contains a word.** The `in` operator checks whether a piece of text occurs inside another string. The check is case sensitive.

45. **Read a character by its index.** A string index selects one character. Index 0 is the first character, and index -1 is the last.

46. **Build a message with string addition.** The `+` operator joins strings together. Both sides must be strings; use an f-string to include a number.

47. **Convert a whole number from text.** `int("90")` converts digit text to the integer 90, so you can do arithmetic with it. The result is an `int`.

48. **Convert a decimal number from text.** `float("94.5")` converts decimal text to the number 94.5. The result is a `float`.

49. **Expect bad number text to raise an error.** `int("ninety")` cannot convert a word to a whole number, so Python raises `ValueError`. `assertRaises` checks that expected error.

50. **Round an average for display.** `round(average, 1)` returns a number rounded to one decimal place. The original value is unchanged.

51. **Get a quotient and remainder together.** `divmod(95, 10)` returns `(9, 5)`: 10 fits into 95 nine times, with 5 left over. Tuple unpacking stores each result by name.

52. **Use remainder to find even grades.** `grade % 2` is the remainder after dividing by 2. Even grades have remainder 0, so Craig (90) and Hancho (60) are selected.

53. **Find the lowest grade with min.** `min()` returns the smallest value in the grades. Here Annete has the lowest grade, 45.

54. **Find the highest grade with max.** `max()` returns the largest value in the grades. Here Craig has the highest grade, 90.

55. **Sort grades from highest to lowest.** `sorted(..., reverse=True)` puts the highest grade first. It returns a new list; the course roster stays in its original order.

56. **Add an item to a list.** `append()` adds one item to the end of a list. Here it changes the separate `names` list; the course still has three students.

57. **Remove an item from a list.** `.remove("Hancho")` deletes the first matching value from a list. The course roster is unchanged because `names` is a separate list.

58. **Check whether a student is in a list.** `assertIn(value, list)` checks that a list contains a value. This example checks both the student object and the student name.

59. **Check whether a student is absent.** `assertNotIn` checks that Maya is not enrolled. The test frees a place, adds her, and uses `assertIn` to confirm she is on the roster.

60. **Read tuple values by index.** Tuples use the same index rules as lists: index 0 selects the first value and index -1 selects the last.

61. **Tuples cannot be changed in place.** Tuples are immutable: assigning a new value to one of their indexes raises `TypeError`. The original name remains Craig.

62. **Read dictionary keys.** `.keys()` provides a view of the dictionary keys. Converting it to a set makes the test compare names without depending on display formatting.

63. **Read dictionary values.** `.values()` provides the dictionary values in insertion order. This gradebook was built from the students in roster order, so its values are 90, 60, 45.

64. **Loop through dictionary key and value pairs.** `.items()` returns each dictionary entry as a `(key, value)` pair. Converting it to a list makes the three pairs easy to inspect.

65. **Change a dictionary value.** Assigning `gradebook["Craig"] = 95` updates that dictionary entry. It does not change Craig's grade on the student object.

66. **Remove and return a dictionary value.** `.pop("Annete")` returns 45 and removes that key from the dictionary. Annete's actual student grade is unchanged.

67. **Find shared values with set intersection.** Set `.intersection()` returns values that occur in both sets. Only grade 90 is in both examples.

68. **Combine values with set union.** Set `.union()` combines values and removes duplicates. It returns a new set, leaving `class_grades` unchanged.
