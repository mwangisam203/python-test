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
print(course.add_student(stud1))


# Example 2 Inheritance Claases 
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def what_i_do(self):
        print(f"I am {self.name}, and I am {self.age} years old")

    def speech(self):
        print("I am too tired to speak, pleas!!")

class Pig(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speech(self):
        print("ngroooollll !!")

    def what_i_do(self):
        print(f"I am {self.name}, and Im {self.age} years old, my color is {self.color}")

class Monkey(Animal):
    def speech(self):
        print("Chappy chappy chapping !!")

an1 = Animal("dogma", 8)
an1.what_i_do()

an2 = Monkey("Kabanzy", 13)
an2.speech()
an2.what_i_do()


        



        
        