import java.util.Scanner;

class Calculator{


      public static void main(String[] args) {
        
     // initiazlize scanner and calculator
        Scanner scanner = new Scanner(System.in);

// enter user input1
        System.out.println("Enter first number:");
        double num1 = scanner.nextDouble();
// enter user input2
        System.out.println("Enter second number:");
        double num2 = scanner.nextDouble();
        System.err.println("additon is " + (num1 + num2));
        System.err.println("subtraction is " + (num1 - num2));
        System.err.println("multiplication is " + (num1 * num2));
        if(num2 != 0){
        System.err.println("division is " + (num1 / num2));
        } else {
        System.err.println("division is not possible");
        }

      
// close scanner
        scanner.close();
    }
}

