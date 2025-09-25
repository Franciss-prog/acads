import java.util.Scanner;

public class dowhileloop {
  public static void main(String[] args) {
    // initialzie Scanner
    Scanner scanner = new Scanner(System.in);
    String password = "12345";
    String enteredPassword;

    do {
      // sk user to input password
      System.out.print("Enter password: ");
      enteredPassword = scanner.nextLine();

      if (!enteredPassword.equals(password)) {
        System.out.println("Wrong password");
      }
    } while (!enteredPassword.equals(password));
    System.out.println("Welcome to login system");
    scanner.close();
  }
}
