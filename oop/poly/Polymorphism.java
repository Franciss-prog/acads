import java.util.Scanner;

// Parent class
class Vehicle {

  void info() {
    System.out.println("This is a vehicle");
  }

  void info(String brand, int year, String color, String transmission, String convertible) {
    System.out.println("Brand: " + brand);
    System.out.println("Year: " + year);
    System.out.println("Color: " + color);
    System.out.println("Transmission: " + transmission);
    System.out.println("Convertible: " + convertible);
  }

  int speed() {
    return 0;
  }
}

class Car extends Vehicle {
  @Override
  int speed() {
    return 150;
  }
}

class Motorcycle extends Vehicle {
  @Override
  int speed() {
    return 200;
  }
}

public class Polymorphism {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);

    // ---------------- CAR INPUT ----------------
    Car car = new Car();
    System.out.println("=== Enter Car Details ===");

    System.out.print("Brand: ");
    String carBrand = scanner.nextLine();

    System.out.print("Year: ");
    int carYear = scanner.nextInt();
    scanner.nextLine(); // clear buffer

    System.out.print("Color: ");
    String carColor = scanner.nextLine();

    System.out.print("Transmission: ");
    String carTransmission = scanner.nextLine();

    System.out.print("Convertible (Yes/No): ");
    String carConvertible = scanner.nextLine();

    // print car details
    System.out.println("\n--- Car Information ---");
    car.info(carBrand, carYear, carColor, carTransmission, carConvertible);

    Motorcycle motorcycle = new Motorcycle();
    System.out.println("\n=== Enter Motorcycle Details ===");

    System.out.print("Brand: ");
    String motoBrand = scanner.nextLine();

    System.out.print("Year: ");
    int motoYear = scanner.nextInt();
    scanner.nextLine(); // clear buffer

    System.out.print("Color: ");
    String motoColor = scanner.nextLine();

    System.out.print("Transmission: ");
    String motoTransmission = scanner.nextLine();

    System.out.print("Convertible (Yes/No): ");
    String motoConvertible = scanner.nextLine();

    // print motorcycle details
    System.out.println("\n--- Motorcycle Information ---");
    motorcycle.info(motoBrand, motoYear, motoColor, motoTransmission, motoConvertible);

    int carSpeed = car.speed();
    int motoSpeed = motorcycle.speed();

    System.out.println("\nCar speed: " + carSpeed + " km/h");
    System.out.println("Motorcycle speed: " + motoSpeed + " km/h");

    if (motoSpeed > carSpeed) {
      System.out.println("Motorcycle is faster");
    } else if (carSpeed > motoSpeed) {
      System.out.println("Car is faster");
    } else {
      System.out.println("Both vehicles have the same speed");
    }

    scanner.close();
  }
}
