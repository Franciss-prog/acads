import java.util.Scanner;

class setThree {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Set 3: Number comparison system");

        // ask user to input two numbers
        System.out.print("Enter first number: ");
        int num1 = scanner.nextInt();
        System.out.print("Enter second number: ");
        int num2 = scanner.nextInt();


        // print which number is greater than and print || if both numbers are equal
        if (num1 > num2) {
            System.out.println(num1);
        } 
        if (num2 > num1) {
            System.out.println(num2);
        } 

        if (num1 == num2) {

            // print even or odd if both numbers are equal
            if (num1 % 2 == 0 && num2 % 2 == 0) {
                System.out.println("both numbers are even");
            } 
            else if (num1 % 2 != 0 && num2 % 2 != 0) {
                System.out.println("both numbers are odd");
            }

        }
    }
     
}