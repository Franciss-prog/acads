import java.util.Scanner;

class Calculator{
// addition
void add(int num1, int num2) {
        System.out.println(num1 + num2);
    }
    // subtraction
    void subtract(int a, int b) {
        System.out.println(a - b);
    }
    // multiplication
    void multiply(int a, int b) {   
        System.out.println(a * b);
    }
    // division
    void divide(int a, int b) {     
        if (b != 0) {
            System.out.println(a / b);
        } else {
            System.out.println("Error: Division by zero");
        }
    }

      public static void main(String[] args) {
        
     // initiazlize scanner and calculator
        Scanner scanner = new Scanner(System.in);
        Calculator calculator = new Calculator();

// enter user input1
        System.out.println("Enter first number:");
        int num1 = scanner.nextInt();
// enter user input2
        System.out.println("Enter second number:");
        int num2 = scanner.nextInt();
// choose operation
        System.out.println("Choose operation: +, -, *, /");
        char operation = scanner.next().charAt(0);
// perform operation
        switch (operation) {
            case '+':
                calculator.add(num1, num2);
                break;
            case '-':
                calculator.subtract(num1, num2);
                break;
            case '*':
                calculator.multiply(num1, num2);
                break;
            case '/':
                calculator.divide(num1, num2);
                break;
            default:
                System.out.println("Invalid operation");
                break;
        }
// close scanner
        scanner.close();
    }
}

