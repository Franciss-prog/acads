class Person:
    # setter
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # getter
    def get_name(self):
        return self.name

    def get_age(self):
        return self.age


# GET THE inout from the user and acccess it by getter functions
name = input("Enter your name: ")
age = int(input("Enter your age: "))


newPerson = Person(name, age)

print(newPerson.get_name())
print(newPerson.get_age())
