class Student():
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade  # max grade = 100

    def get_grade(self):
        return self.grade
    
class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False
    
    def get_average_grade(self):
        value = 0
        for student in self.students:
            value += student.get_grade()

        return value / len(self.students)

stud1 = Student("Craig", 16, 90)
stud2 = Student("Hancho", 15, 98)
stud3 = Student("Annete", 17, 89)

course = Course("Biochem", 2)

course.add_student(stud1)
course.add_student(stud2)

print(course.get_average_grade())





        
        