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

69. **Divide whole numbers with floor division.** `//` divides and rounds down to a whole number; `/` gives a regular division result. So `95 // 10` is 9 while `95 / 10` is 9.5.

70. **Find how far a number is from zero.** `abs()` returns a number's distance from zero, so the result is never negative.

71. **Insert a value at a chosen position.** `insert(1, "Maya")` puts Maya at index 1 and shifts the later items right.

72. **Add several items with extend.** `extend()` adds every item from another iterable to the end of a list.

73. **Reverse a list in place.** `.reverse()` changes the list it is called on. Here the separate names list is reversed; course enrollment order stays the same.

74. **Find an item position with index.** `.index("Hancho")` returns 1 because Hancho is at index 1. It raises `ValueError` if the value is absent.

75. **Take every other list item with a slice.** The third slice value is the step size. `[::2]` starts at the beginning and selects every second item.

76. **Use range to repeat a loop.** `range(1, 5)` counts from 1 up to, but does not include, 5. `list()` makes its values easy to inspect.

77. **Iterate over a list backwards.** `reversed(names)` provides the values in reverse order without changing `names`. Convert it to a list to compare all values.

78. **Set a dictionary default with setdefault.** `.setdefault(key, default)` adds a missing key with its default. For a key that already exists, it returns the current value.

79. **Update a dictionary with another dictionary.** `.update()` replaces values for matching keys and adds new keys from another dictionary.

80. **Delete a dictionary entry by key.** `del gradebook["Maya"]` removes the entry with that key. Deleting a missing key raises `KeyError`.

81. **Build a dictionary for passing students.** A condition in a dictionary comprehension filters its entries. This example keeps names and grades for students with a passing grade.

82. **Check whether one set fits inside another.** `.issubset()` returns `True` if every value in the first set also occurs in the second set.

83. **Find values that occur in only one set.** Set `.difference()` returns values from the first set that are absent from the second.

84. **Choose a value with a conditional expression.** `value_if_true if condition else value_if_false` chooses one of two values. Craig gets `"pass"`; Annete gets `"try again"`.

85. **Add values with a for loop.** The loop adds one grade at a time to `total`. Starting at zero gives a final total of 90 + 60 + 45 = 195.

86. **Stop a loop with break.** `break` exits the loop immediately. This loop stops when it finds the first passing student, Craig.

87. **Repeat a task with a while loop.** `while` repeats as long as its condition is true. Updating `steps` each time eventually makes the condition false.

88. **Write a small reusable function.** A function groups steps under a name. `describe()` can format different students without copying the same expression.

89. **Handle a conversion error with try and except.** `try` runs code that may fail. `except ValueError` handles this invalid number text and assigns a fallback value.

90. **Check for no result with is None.** `is None` checks for the special no-result value `None`. Use it when a lookup might not find anything.

91. **Capitalize a string.** `capitalize()` makes the first character uppercase and the remaining characters lowercase.

92. **Make each word start with a capital.** `.title()` capitalizes the start of each word in a string.

93. **Swap the case of each letter.** `.swapcase()` makes lowercase letters uppercase and uppercase letters lowercase.

94. **Find text inside a string.** `.find()` returns the index of the first match. If the text is absent, it returns -1 instead of raising an error.

95. **Split text into two parts.** `.partition(separator)` returns a three item tuple: the text before the first separator, the separator, and the text after it.

96. **Remove a known prefix.** `.removeprefix()` removes the given text only when it appears at the start of the string.

97. **Check whether text contains only decimal digits.** `.isdecimal()` is true for text made only of decimal digits. A decimal point and words make it false.

98. **Pad a number with zeros for display.** The f-string format `03` displays a number in a width of three, padding the front with zeros.

99. **Select characters with a string slice.** A string slice uses a start index and an excluded stop index. `name[1:4]` selects indexes 1, 2, and 3.

100. **Count an item in a list.** `.count(value)` reports how many times a value occurs in a list. A value that does not occur has a count of zero.

101. **Pop the last item from a list.** Calling `.pop()` without an index removes and returns the last list item.

102. **Clear all items from a list.** `.clear()` removes all items from that list. The separate course roster is unchanged.

103. **Sort a list in place.** `.sort()` changes the list itself and returns `None`. Use `sorted()` when you need a new sorted list.

104. **Replace a list item by index.** Assigning to a list index replaces the item at that position. Index 1 is the second item.

105. **Unpack the first item and the rest.** A starred unpacking target collects zero or more remaining values into a list.

106. **Count a value in a tuple.** Tuples also provide `.count()` to count repeated values. The tuple remains unchanged.

107. **Add a value to a set.** `.add()` inserts a value into a set. A set stores each value once.

108. **Discard a value from a set safely.** `.discard()` removes a value if present and does nothing if absent. `.remove()` instead raises `KeyError` for an absent value.

109. **Check whether a set contains another set.** `.issuperset()` returns true when the set contains every value in the other set.

110. **Add several values to a set.** Set `.update()` adds all values from another collection. Repeated values are still kept only once.

111. **Create dictionary keys with one default value.** `dict.fromkeys(keys, value)` creates a dictionary with each key set to the given value.

112. **Copy a dictionary.** `.copy()` makes a separate dictionary. Adding a key to the copy leaves the original dictionary unchanged.

113. **Pop the most recently added dictionary entry.** `.popitem()` removes and returns the most recently added key and value as a pair.

114. **Use in to check dictionary keys.** For a dictionary, `in` checks keys. Use `.values()` when you want to check the stored values.

115. **Raise a number to a power.** The `**` operator raises the left number to the power on the right.

116. **Compare a value against a range.** `0 <= grade <= 100` checks both comparisons. It means the grade is at least zero and at most 100.

117. **Convert a value to true or false.** `bool()` converts a value to `True` or `False`. Zero and an empty string are false; a nonzero number and nonempty string are true.

118. **Update a number with an augmented assignment.** `+=` adds to a variable and stores the result back. `-=` works the same way for subtraction.

119. **Calculate open course places.** Subtract the current enrollment count from the maximum capacity to find the number of remaining places.

120. **Give a function argument a default.** A function uses a default argument value when the caller leaves that argument out. A caller can supply a different value.

121. **Collect extra function arguments with args.** `*numbers` collects any number of positional arguments into a tuple that the function can loop over.

122. **Collect named function arguments with kwargs.** `**details` collects named arguments into a dictionary, so the function can look up each value by name.

123. **Apply a function to every item with map.** `map(function, values)` applies a function to each value. Converting it to a list shows the results.

124. **Keep matching items with filter.** `filter(function, values)` keeps values where the function returns true. This example keeps grades of 60 or higher.

125. **Check a value type with isinstance.** `isinstance(value, type)` checks whether a value has the requested type. Numeric text such as `"90"` is still a string.

126. **Combine conditions with and.** `and` is true only when both conditions are true. The example checks that a grade is at least 60 and at most 100.

127. **Use or to provide a default for None.** `or` returns its first truthy value, or the second value if the first is false. It can provide a fallback for `None`; zero also counts as false.

128. **Invert a condition with not.** `not` flips a boolean result. The passing student does not fail; Annete does not pass.

129. **Compare values with equality.** `==` checks whether values are equal. `is` checks whether two names refer to the exact same object.

130. **Convert a number to text.** `str()` converts a value to text. The result `"90"` is a string, so use `int()` if you need number arithmetic.

131. **Convert a decimal to a whole number.** `int()` drops the fractional part and moves toward zero. It does not round to the nearest integer.

132. **Calculate a power with pow.** `pow(base, exponent)` raises the base to the exponent, like the `**` operator.

133. **Use operator precedence.** Multiplication happens before addition, so `2 + 3 * 4` evaluates to 14.

134. **Use parentheses to set the order.** Parentheses make the addition happen before multiplication. This expression evaluates to 20.

135. **Write a negative number.** A minus sign before a number makes it negative. Applying unary minus to a negative number makes it positive.

136. **Swap two values in one assignment.** Python evaluates both values on the right before assigning them. This makes it easy to swap two variables.

137. **Read an item from a nested list.** Use one index for the outer list and another for the inner list. Here `grades[0][1]` is the second value in the first row.

138. **Unpack pairs while looping.** When a loop receives a tuple of two values, it can unpack them into two variables on each iteration.

139. **Loop through dictionary entries.** `.items()` gives a dictionary's key and value pairs. The loop unpacks each pair into `name` and `grade`.

140. **Pass a function argument by name.** Keyword arguments identify each value by parameter name. Their order can differ from the function definition.

141. **Align text inside an f-string.** The `>` format aligns text to the right and `<` aligns it to the left within the requested width.

142. **Pad digit text with zeros.** `.zfill(width)` adds zeros to the left until a string reaches the requested width.

143. **Split text at line breaks.** `.splitlines()` separates a string at its line breaks and returns the individual lines.

144. **Check whether letters are uppercase.** `.isupper()` is true when a string has at least one cased letter and all its cased letters are uppercase.

145. **Check whether text contains only spaces.** `.isspace()` is true when the string contains one or more whitespace characters and nothing else. Empty text returns false.

146. **Find values that differ between sets.** Set `.symmetric_difference()` returns values that appear in either set, but not in both.

147. **Make a set that cannot be changed.** `frozenset()` creates an immutable set. Like a regular set, it keeps each value only once.

148. **Read a value from a nested dictionary.** A dictionary can contain another dictionary as a value. Use one key for each level to reach the nested value.

149. **Change a value inside a nested list.** Use indexes from the outside in to change a value inside a nested list.

150. **Add up values from a comprehension.** A generator expression can select values for `sum()`. Here only passing grades, 90 and 60, are added.

151. **Round to two decimal places.** Pass 2 as the second argument to `round()` to round a number to two decimal places.

152. **Format a number as a percentage.** The `%` f-string format multiplies a fraction by 100 and adds a percent sign. `.0%` displays no decimal places.

153. **Read a function docstring.** A string directly inside a function is its docstring. Python stores it in the function's `__doc__` attribute.

154. **Require a named function argument.** Parameters after `*` are keyword only. The caller must use the parameter name, such as `name="Craig"`.

155. **Return early when a condition is met.** A `return` ends the function immediately. This lets a function handle a simple case before continuing to another return.

156. **Choose a label inside a list comprehension.** A conditional expression can choose a value for each item in a list comprehension.

157. **Flatten rows from a nested list.** A second `for` in a comprehension can visit items inside each row of a nested list.

158. **Remove a dictionary key with a fallback.** Dictionary `.pop(key, default)` returns and removes an existing value. For a missing key, it returns the default.

159. **Clear a dictionary.** `.clear()` removes all entries from the dictionary in place.

160. **Count unique values with a set.** Converting a list to a set removes repeated values. `len()` then counts the unique grades.

161. **Create a tuple with one item.** A comma makes a one item tuple. Parentheses alone, as in `(90)`, do not.

162. **Join tuples together.** The `+` operator joins tuples into a new tuple.

163. **Append a list as one nested item.** `append()` adds its argument as a single item. Appending a list creates a nested list.

164. **Sort names by their length.** `key=len` tells `sorted()` to compare each name by its length. Names with equal lengths keep their original order.

165. **Sort uppercase and lowercase text.** Normal string sorting is case sensitive. Uppercase letters sort before lowercase letters here.

166. **Compare text without case differences.** `.casefold()` makes text lowercase for case insensitive comparisons, including some characters that `.lower()` leaves different.

167. **Remove a known suffix.** `.removesuffix()` removes the given text only when it appears at the end of the string.

168. **Limit how many times split separates text.** `split(separator, maxsplit=1)` splits once, leaving the rest of the text together.

169. **Split text from the right.** `.rsplit()` starts at the right side. With a single split, it separates the final field.

170. **Convert between a character and its code.** `ord()` returns a character's Unicode number; `chr()` converts that number back to a character.

171. **Encode and decode UTF-8 text.** `.encode("utf-8")` turns text into bytes. Decoding those bytes with UTF-8 recovers the original text. The accented character takes two bytes.

172. **Use math sqrt to find a square root.** Importing the standard library `math` module gives you `sqrt()` for square roots.

173. **Round a number upward with ceil.** `math.ceil()` rounds upward to the nearest integer.

174. **Round a number downward with floor.** `math.floor()` rounds downward to the nearest integer.

175. **Find the average with statistics mean.** The standard library `statistics.mean()` calculates the arithmetic average of a list of numbers.

176. **Count repeated values with Counter.** `collections.Counter` counts how often each item appears.

177. **Find the most common value.** `.most_common(1)` returns a list containing the most common value and its count.

178. **Give missing dictionary keys a list.** `defaultdict(list)` automatically creates an empty list the first time a missing key is used.

179. **Use a deque as a first in first out queue.** `deque` supports adding items at either end. `popleft()` removes the oldest item from the left side.

180. **Rotate items in a deque.** `.rotate(1)` moves the last item to the front. A negative number rotates in the other direction.

181. **Join iterables with chain.** `itertools.chain()` lets one loop visit multiple sequences in order.

182. **Create pairs with product.** `itertools.product()` makes every possible pair from the supplied groups.

183. **Repeat a value with itertools.** `itertools.repeat(value, count)` provides the value the requested number of times.

184. **Take part of an iterator with islice.** `islice()` takes a start, stop, and step, much like a list slice, while reading an iterator.

185. **Find a greatest common divisor.** `math.gcd()` returns the largest integer that divides both inputs evenly.

186. **Calculate a factorial.** `math.factorial(5)` multiplies 5 × 4 × 3 × 2 × 1. By definition, zero factorial is 1.

187. **Compare close floating point numbers.** `math.isclose()` checks whether two floating point results are close enough, allowing for small rounding differences.

188. **Remove a decimal part without rounding.** `math.trunc()` removes the decimal part and moves toward zero for positive and negative numbers.

189. **Find a base ten logarithm.** `math.log10(value)` answers which power of ten gives that value.

190. **Add decimals accurately with fsum.** `math.fsum()` adds floating point values while reducing small rounding errors.

191. **Find the middle value with median.** `statistics.median()` returns the middle value after ordering the data. For an even number of values, it averages the middle pair.

192. **Find the most frequent value with mode.** `statistics.mode()` returns the value that occurs most often.

193. **Measure population spread with pstdev.** `statistics.pstdev()` calculates the population standard deviation, a measure of how spread out the values are.

194. **Read a file name from a path.** `Path.name` returns the last part of a path. It works on the path text without opening a file.

195. **Read a file suffix from a path.** `Path.suffix` returns the final file extension, including its leading dot.

196. **Read the parent folder name.** `Path.parent` returns the containing path. Its `.name` is the folder `reports`.

197. **Change a path suffix.** `.with_suffix()` returns a new path with the requested extension and leaves the original path unchanged.

198. **Read the parts of a path.** `.parts` returns the components of a path as a tuple.

199. **Check whether a path is absolute.** An absolute path starts from the filesystem root. A relative path is interpreted from the current folder.

200. **Format text with format.** `.format()` puts supplied values into `{}` placeholders in a string.

201. **Show quotation marks with the repr conversion.** The `!r` f-string conversion uses `repr()` so that the resulting text shows string quotation marks.

202. **Combine dictionaries with unpacking.** `**` inside a dictionary literal copies entries from another dictionary.

203. **Find shared set values with an operator.** The `&` operator finds the intersection: values present in both sets.

204. **Combine sets with the union operator.** The `|` operator combines sets and keeps each value only once.

205. **Check set containment with comparisons.** For sets, `<=` checks whether every item in the left set is also in the right set.

206. **Use loop else when no item matched.** A loop's `else` block runs when the loop finishes without `break`. Here Maya is absent, so the `else` runs.

207. **Use try else after a successful conversion.** The `else` block after `try` runs only when the `try` block completes without an exception.

208. **Use finally to always run cleanup code.** The `finally` block runs after `try`, whether the work succeeded or raised an error. It is often used for cleanup.

209. **Raise an error for invalid input.** `raise ValueError(...)` stops a function when its input is invalid. `assertRaisesRegex` checks both the error type and message.

210. **Add type hints to a function.** Type hints document the expected input and return types. Python records them in `__annotations__`; they do not automatically enforce types.

211. **Keep a running total with accumulate.** `itertools.accumulate()` returns each running total, which is useful for tracking a sum as values arrive.

212. **Choose pairs with combinations.** `itertools.combinations(items, 2)` creates pairs without repeating an item or reversing the same pair.

213. **Arrange items with permutations.** `itertools.permutations()` lists possible orderings. With two different items there are two orders.

214. **Multiply values with prod.** `math.prod()` multiplies all the values in an iterable. The product of an empty iterable is defined as 1.

215. **Find an integer square root.** `math.isqrt()` returns the whole-number square root, rounding down when the input is not a perfect square.

216. **Give a number the sign of another.** `math.copysign(value, sign)` takes the size of the first number and the sign of the second.

217. **Convert degrees to radians.** `math.radians()` converts degrees to radians, the angle unit used by many math functions.

218. **Convert radians to degrees.** `math.degrees()` converts radians back to degrees.

219. **Find every most common value with multimode.** `statistics.multimode()` returns every value tied for most frequent, in the order each first appears.

220. **Split ordered data into quartiles.** `statistics.quantiles(data, n=4)` divides ordered data into four groups and returns the three cut points.

221. **Read a file name without its extension.** `Path.stem` returns the final path name without its last suffix.

222. **Read every suffix in a file name.** `Path.suffixes` returns all extensions, which helps with names such as `archive.tar.gz`.

223. **Change the name at the end of a path.** `.with_name()` returns a new path with a replacement final name, while leaving the original unchanged.

224. **Display a path with forward slashes.** `.as_posix()` displays path parts with forward slashes, regardless of the platform separator.

225. **Check whether a path is inside another path.** `.is_relative_to()` checks whether a path begins with the given parent path. It does not access the filesystem.

226. **Create a calendar date.** `date(year, month, day)` creates a calendar date with separate year, month, and day values.

227. **Format a date as ISO text.** `.isoformat()` writes a date in the consistent `YYYY-MM-DD` format.

228. **Read the weekday number from a date.** `.weekday()` numbers Monday as 0 and Sunday as 6.

229. **Add days to a date.** `timedelta(days=...)` represents a duration that can be added to a date.

230. **Subtract dates to find a duration.** Subtracting one date from another returns a duration. Its `.days` value is the number of days between them.

231. **Parse a date from text.** `datetime.strptime(text, format)` reads text using the format you describe. `%Y`, `%m`, and `%d` mean year, month, and day.

232. **Format a date with strftime.** `.strftime()` turns a date into text using format codes such as `%Y` for year and `%m` for month.

233. **Check whether a year is a leap year.** `calendar.isleap(year)` returns whether the year has a leap day.

234. **Find the number of days in a month.** `calendar.monthrange(year, month)` returns the weekday of the first day and the number of days in that month. Monday is 0.

235. **Find digit groups with a regular expression.** `re.findall()` returns every match. The pattern `\d+` means one or more digits.

236. **Replace repeated spaces with one space.** `re.sub(pattern, replacement, text)` replaces every section of text that matches a pattern. `\s+` matches one or more spaces.

237. **Match an entire string with a pattern.** `re.fullmatch()` succeeds only when the pattern matches the entire string. `\d{3}` means exactly three digits.

238. **Convert a dictionary to JSON text.** `json.dumps()` turns Python data into JSON text. `sort_keys=True` makes dictionary keys appear in sorted order.

239. **Read JSON text into Python values.** `json.loads()` reads JSON text and creates the corresponding Python dictionary.

240. **Round trip nested data through JSON.** Encoding data with `json.dumps()` and reading it with `json.loads()` preserves nested lists and dictionaries.

241. **Pretty-print JSON with an indent.** json.dumps() accepts `indent` to make JSON easier to read. An indent of 2 adds two spaces for each nested level.

242. **Keep unicode characters in JSON text.** By default, `json.dumps()` escapes non-ASCII characters. `ensure_ascii=False` keeps characters such as `é` readable in the result.

243. **Remove extra spaces from JSON.** The `separators` option controls punctuation spacing. Using `(',', ':')` makes compact JSON text.

244. **Read a JSON array as a list.** A JSON array becomes a Python list when `json.loads()` reads it.

245. **Read JSON booleans as Python booleans.** JSON `true` and `false` become Python `True` and `False`.

246. **Read JSON null as None.** JSON `null` maps to Python `None`.

247. **Catch invalid JSON text.** Malformed JSON raises `json.JSONDecodeError`, which is a `ValueError` subclass.

248. **Turn dictionary keys into JSON strings.** JSON object keys are strings. Integer dictionary keys are converted to text during encoding.

249. **Find a match anywhere in text.** `re.search()` looks through the text and returns a match object for the first match, or `None`.

250. **Capture parts of a regular expression match.** Parentheses create capture groups. `group(1)` returns the text captured by the first pair of parentheses.

251. **Split text with a regular expression.** `re.split()` divides text wherever its pattern matches. `\s+` handles one or more whitespace characters.

252. **Match text without case sensitivity.** Pass `re.IGNORECASE` to make a regular expression match uppercase and lowercase letters alike.

253. **Require a pattern at the start.** The `^` anchor matches the beginning of the text.

254. **Require a pattern at the end.** The `$` anchor matches the end of the text.

255. **Make a regular expression part optional.** A question mark makes the preceding pattern optional. Here, the letter `s` may appear zero or one times.

256. **Match one character from a group.** Square brackets define a character class. `[ABC]` matches one of those three letters.

257. **Find a whole word with a boundary.** The `\b` pattern marks a word boundary, so it can find a word without matching that text inside a longer word.

258. **Limit regular expression replacements.** `re.sub()` accepts `count` to limit how many matches it replaces.

259. **Compare calendar dates.** Date objects can be compared in chronological order.

260. **Count days from a date ordinal.** `toordinal()` gives a date an integer day number. Later dates have larger ordinal values.

261. **Create a date with one changed part.** `date.replace()` returns a new date with selected fields changed and leaves the original intact.

262. **Read a time difference in days.** Subtracting two dates produces a `timedelta`; its `days` attribute gives the day difference.

263. **Add a week to a date.** A `timedelta` can be created with weeks and added to a date.

264. **Format a date with its weekday name.** `%A` formats the full weekday name for a date.

265. **Format a date as a day number.** `%j` formats a date as its day number within the year, from 001 to 366.

266. **Parse a time from text.** `datetime.strptime()` reads a time string when given a matching format.

267. **Format a time with a 24 hour clock.** `%H:%M` formats the hour and minute using a 24 hour clock.

268. **Read date and time fields.** A `datetime` stores date fields and time fields that can be read by name.

269. **Find a right triangle hypotenuse.** `math.hypot(x, y)` calculates the Euclidean distance from the origin to `(x, y)`.

270. **Find a floating point remainder.** `math.fmod()` returns the remainder after division for floating point values.

271. **Raise a number to a power.** `math.pow()` raises its first argument to the power of its second and returns a float.

272. **Calculate an exponential value.** `math.exp(x)` returns e raised to the power `x`.

273. **Find a natural logarithm.** `math.log()` returns the natural logarithm. The natural logarithm of `e` is 1.

274. **Check whether a number is finite.** `math.isfinite()` is true for ordinary finite numbers and false for infinity.

275. **Recognize an infinite number.** `math.isinf()` checks whether a number is positive or negative infinity.

276. **Recognize a not-a-number value.** `math.isnan()` checks for a NaN value, which is used to represent an undefined numeric result.

277. **Preserve a number while changing its sign.** `math.copysign()` takes the magnitude from one value and the sign from another.

278. **Use the tau circle constant.** `math.tau` is the circle constant equal to two times `math.pi`.
