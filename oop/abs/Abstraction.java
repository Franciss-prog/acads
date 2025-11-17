
// Abstract class
import java.util.Scanner;

abstract class Car {
  String brand = "Toyota";

  abstract void startEngine();

  abstract void stopEngine();

  void showBrand() {
    System.out.println("Car Brand: " + brand);
  }
}

// Subclass Toyota Vios
class ToyotaVios extends Car {

  @Override
  void startEngine() {
    System.out.println("Toyota Vios engine started using push button.");
  }

  @Override
  void stopEngine() {
    System.out.println("Toyota Vios engine stopped.");
  }

  void showModel() {
    System.out.println("Model: Toyota Vios 2024");
  }
}

// Main class
public class Abstraction {
  public static void main(String[] args) {
    Car myCar = new ToyotaVios(); // Abstraction + Polymorphism
    Scanner scanner = new Scanner(System.in);
    // ask the user if the user want to start
    System.out.print("Do you want to start the engine? (yes/no): ");
    String start = scanner.nextLine();
    if (start.equals("yes")) {
      myCar.startEngine();
    } else {
      myCar.stopEngine();
    }

    // ask the user if the user want to stop
    System.out.print("Do you want to stop the engine? (yes/no): ");
    String stop = scanner.nextLine();
    if (stop.equals("yes")) {
      myCar.stopEngine();
    } else {
      myCar.startEngine();
    }
    // To access showBrand(), cast to ToyotaVios
    ((ToyotaVios) myCar).showBrand();
    // To access showModel(), cast to ToyotaVios
    ((ToyotaVios) myCar).showModel();
  }
}
