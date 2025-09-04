import java.util.Scanner;

class Circle {

void getArea(int radius, double PI) {
    double area = PI * Math.pow(radius, 2);
    System.out.println("Area of the circle: " + area);
}

 public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    Circle circle = new Circle();
    final double PI = 3.14;


    System.out.println("Enter radius of the circle:");
    double radius = scanner.nextDouble();

    circle.getArea(radius, PI);

    scanner.close();
    
    }  
}

