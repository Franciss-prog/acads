# Parent class
class Vehicle:
    def __init__(self, brand, fuel):
        self.brand = brand
        self.fuel = fuel  # amount of fuel in liters


# Subclass
class Car(Vehicle):
    def __init__(self, brand, fuel, doors):
        Vehicle.__init__(self, brand, fuel)  # call parent constructor
        self.doors = doors

    def drive(self, distance):
        fuel_needed = distance * 0.1  # assume 0.1 liter per km
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"{self.brand} drove {distance} km. Fuel left: {self.fuel}")
        else:
            print(f"Not enough fuel to drive {distance} km!")


# Test
my_car = Car("Toyota", 50, 4)
my_car.drive(100)  # drives 100 km
my_car.drive(500)  # tries to drive more than fuel allows
