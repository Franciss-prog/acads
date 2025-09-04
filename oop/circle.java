import java.util.Scanner;

class Circle {

void getArea(int radius) {
    double area = Math.PI * radius * radius;
    System.out.println("Area of the circle: " + area);
}

 public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    Circle circle = new Circle();

    System.out.println("Enter radius of the circle:");
    int radius = scanner.nextInt();

    circle.getArea(radius);

    scanner.close();
    
    }  
}

