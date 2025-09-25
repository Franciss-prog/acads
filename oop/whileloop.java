import java.util.Scanner;

public class whileloop {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    // start and end
    int start = 1;
    int sum = 0;

    // ask user to input ending number
    System.out.print("Enter an number: ");
    int end = scanner.nextInt();

    // loop the starting and ending and print the number
    while (start <= end) {
      // add the sum of start
      sum += start;
      System.out.println("Numbers: " + " " + start);
      start++;
    }

    System.out.println("Sum: " + " " + sum);
    scanner.close();
  }
}
