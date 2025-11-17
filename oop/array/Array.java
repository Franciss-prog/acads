import java.util.Scanner;

class array {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    // initialize array

    int i = 0;

    // ask user to inputhow many words to input
    System.out.println("How many words do you want to input: ");
    String[] str = new String[scanner.nextInt()];
    // ask user to input string
    System.out.println("Please enter" + " " + str.length + " " + "words: ");
    while (i < str.length) {
      str[i] = scanner.nextLine();
      i++;
    }
    System.out.println("First Element: " + str[0]);
    System.out.println("Last Element: " + str[str.length - 1]);

    // print array
    for (i = 0; i < str.length; i++) {
      System.out.print(str[i]);
      System.out.print(" ");
    }
    scanner.close();
  }
}
