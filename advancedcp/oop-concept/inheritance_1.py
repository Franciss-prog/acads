# main clas
class Animal:
    def speak(self):
        return self


# child class
class Dog(Animal):
    def speak(self):
        print("Woof!")
        print("Aww!")
        print("Bark!")


class Cat(Animal):
    def speak(self):
        print("Meow!")
        print("Purr!")
        print("Psssspss")


dog = Dog()
dog.speak()  # output: Woof!

cat = Cat()
cat.speak()  # output: Meow
