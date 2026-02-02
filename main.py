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

    




        
        