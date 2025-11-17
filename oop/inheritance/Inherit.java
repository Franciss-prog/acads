import java.util.Scanner;

class Vehicle {
  String brand;
  String transmission;
  String model;
  String convertible;
  String color;

  void start() {
    System.out.println("Vehicle is starting...");
  }
}

class Car extends Vehicle {

  void displayInfo() {
    System.out.println("Brand: " + brand);
    System.out.println("Model: " + model);
    System.out.println("Transmission:" + transmission);
    System.out.println("Convertible: " + convertible);
    System.out.println("Color: " + color);
  }
}

public class Inherit {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    Car myCar = new Car();

    System.out.print("What brand do you want? ");
    myCar.brand = scanner.nextLine();
    System.out.print("What model? ");
    myCar.model = scanner.nextLine();
    System.out.print("Enter transmission: ");
    myCar.transmission = scanner.nextLine();
    System.out.print("Enter convertible: ");
    myCar.convertible = scanner.nextLine();
    System.out.print("Enter color: ");
    myCar.color = scanner.nextLine();
    myCar.start();
    myCar.displayInfo();
    scanner.close();
  }
}
