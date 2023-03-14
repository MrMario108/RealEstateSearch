
class Worker():
    name = 0
    @classmethod
    def from_name(self,worker_name):
        print('from_name')
        self.name = worker_name
    @classmethod
    def execute(self):
        if self.name == 0:
            print("0", self.name)
        if self.name == 1:
            print("1", self.name)
        if self.name == 2:
            print("2", self.name)
    
    
x = Worker.from_name(2)

from datetime import date

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def calculate_age(cls, name, birth_year):
        # calculate age an set it as a age
        # return new object
        return cls(name, date.today().year - birth_year)

    def show(self):
        print(self.name + "'s age is: " + str(self.age))

jessa = Student('Jessa', 20)
jessa.show()

# create new object using the factory method
joy = Student.calculate_age("Joy", 1995).show()
#joy.show()