class Shape:
    def area(self):
        print("Area method not implemented")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        print(3.14 * self.radius * self.radius)


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        print(self.width * self.height)


# Test
c = Circle(5)
r = Rectangle(4, 6)
c.area()  # 78.5
r.area()  # 24
