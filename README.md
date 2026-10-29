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
