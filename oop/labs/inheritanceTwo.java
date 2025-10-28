class Vehicle {
    String brand;
    int fuel;

    Vehicle(String brand, int fuel) {
        this.brand = brand;
        this.fuel = fuel;
    }
}

class Car extends Vehicle {
    int doors;

    Car(String brand, int fuel, int doors) {
        super(brand, fuel);
        this.doors = doors;
    }

    void drive() {
        if (fuel > 0) {
            fuel--;
            System.out.println("Driving the " + brand + ". Fuel left: " + fuel);
        } else {
            System.out.println("Out of fuel!");
        }
    }
}
public class inheritanceTwo {
 public static void main(String[] args) { 
  Car car = new Car("Toyota", 100, 4);
  car.drive();
  car.drive();
 }
}
