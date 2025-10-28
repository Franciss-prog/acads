# Inheritance act 2
class Vehicle:
    def __init__(self, brand, fuel):
        self.brand = brand
        self.fuel = fuel


class Car(Vehicle):
    def __init__(self, brand, fuel, doors):
        super().__init__(brand, fuel)  # Calls parent constructor
        self.doors = doors

    def drive(self, distance):
        fuel_needed = distance * 0.1
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"Driving {distance} km. Fuel left: {self.fuel}")
        else:
            print("Not enough fuel!")


# Test
my_car = Car("Toyota", 50, 4)
my_car.drive(100)
