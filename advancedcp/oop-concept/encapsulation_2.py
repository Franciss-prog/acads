class Person:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if age < 0:
            print("Age is not valid, setting age to 0.")
        self._age = max(0, age)


# test
person = Person(30)
print(person.age)  # 30
person.age = -5
print(person.age)  # 0
